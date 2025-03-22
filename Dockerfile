FROM vastai/comfy:v0.3.13-cuda-12.1-pytorch-2.5.1-py311

WORKDIR /workspace

COPY . /workspace/

RUN chmod +x /workspace/start.sh /workspace/comfyui.sh /workspace/api.sh

CMD ["bash", "-c", "/workspace/start.sh"]