import urllib.request
import json

class ComfyUIController:

    @staticmethod
    def queue_prompt(prompt, client_id, port):
        p = {"prompt": prompt, "client_id": client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://localhost:{port}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())
    
    @staticmethod
    async def get_images(ws, jsonwf, client_id, port):
        prompt = ComfyUIController.queue_prompt(jsonwf, client_id, port)
        prompt_id = prompt['prompt_id']
        output_images = {}
        current_node = ""
        while True:
            out = await ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['prompt_id'] == prompt_id:
                        if data['node'] is None:
                            break  # Execution is done
                        else:
                            current_node = data['node']
            else:
                if current_node == 'SaveImageWebsocket':
                    images_output = output_images.get(current_node, [])
                    images_output.append(out[8:])
                    output_images[current_node] = images_output

        return output_images
