import boto3
from botocore.client import Config
import random
import string
import time
import os
import uuid
import subprocess
from fastapi import HTTPException

def cloudfare_upload(object_name, image_data):
    session = boto3.Session()
    s3_client = session.client(
        's3',
        endpoint_url=os.getenv('CR2_ENDPOINT'),
        aws_access_key_id=os.getenv('CR2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('CR2_SECRET_ACCESS_KEY'),
        config=Config(signature_version='s3v4')
    )
    
    s3_client.put_object(
        Bucket=os.getenv('CR2_BUCKET'),
        Key=object_name,
        Body=image_data,
        ContentType='image/png'
    )

def generate_unique_filename():
    random_part = ''.join(random.choice(string.ascii_lowercase) for _ in range(15))
    timestamp = int(time.time())
    filename = f"{random_part}_{timestamp}"
    return filename

def generate_client_id():
    return str(uuid.uuid4())

def restart_comfyui_server(port: int):
    try:
        directory = "/workspace/ComfyUI"
        run_command = f"{directory}/venv/bin/python {directory}/main.py --listen 0.0.0.0 --port {port}"
        
        command = f"screen -dm bash -c 'cd {directory} && {run_command}'"
        
        subprocess.run(command, shell=True)
        return("Server restart attempted in a new screen session.")
    
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
def kill_process_on_port(port):
    try:
        result = subprocess.check_output(f"fuser {port}/tcp 2>/dev/null", shell=True, text=True)
        pids = result.strip().split()
        
        if pids:
            for pid in pids:
                print(f"Killing process {pid} on port {port}")
                os.kill(int(pid), 9)
            print(f"Successfully killed processes on port {port}.")
        else:
            print(f"No process found running on port {port}.")
    except subprocess.CalledProcessError:
        print(f"No process found running on port {port}.")

async def restart_comfyui_servers():
    try:
        for port in [3001, 3002, 3003, 3004]:
            kill_process_on_port(port)
            restart_comfyui_server(port)
        return {"result" : "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
