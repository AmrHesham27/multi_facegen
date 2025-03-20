import json
from requests.FacegenRequest import FacegenRequest
import os
from fastapi import HTTPException
import random
import websockets
from controllers.ComfyUIController import ComfyUIController
from helpers import generate_unique_filename, cloudfare_upload, generate_client_id, restart_comfyui_server
from ports_dict import Facegen_port

class FacegenController:
    port = Facegen_port

    @staticmethod
    async def create(request: FacegenRequest):
        try:
            client_id = generate_client_id()

            prompt = request.prompt
            negative_prompt = request.negative_prompt
            face_image = request.face_image
            width = request.width
            height = request.height
            samples = request.samples
            
            with open(os.path.join("workflows", "5_facegen.json"), "r", encoding="utf-8") as f:
                workflow_jsondata = f.read()
            jsonwf = json.loads(workflow_jsondata)

            jsonwf["22"]["inputs"]["text"] = prompt
            jsonwf["23"]["inputs"]["text"] = negative_prompt
            jsonwf["35"]["inputs"]["url_or_path"] = face_image
            jsonwf["5"]["inputs"]["width"] = width
            jsonwf["5"]["inputs"]["height"] = height
            jsonwf["5"]["inputs"]["batch_size"] = samples

            images_urls = []
            async with websockets.connect(f"ws://localhost:{FacegenController.port}/ws?clientId={client_id}", max_size=7*2**20) as ws:
                images = await ComfyUIController.get_images(ws, jsonwf, client_id, FacegenController.port)

                for node_id in images:
                    for image_data in images[node_id]:
                        """ name = generate_unique_filename()
                        cloudfare_upload(f"images/{name}.png", image_data)
                        images_urls.append(f"{os.getenv('CR2_URL')}/images/{name}.png") """
                        images_urls.append(image_data)

                        """ with open("output.txt", "a") as output_file:
                            output_file.write(f"Image URL: {os.getenv('CR2_URL')}/images/{name}.png\n") """

            
            return {"status": "success", "output": images_urls}

        except OSError as e:
            if '[Errno 111]' in str(e) and 'Connect call failed' in str(e):
                restart_comfyui_server(FacegenController.port)
                raise HTTPException(status_code=500, detail=f"Please try again after1 minute.")
            else:
                print(f"OSError occurred: {str(e)}")
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing data: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
