FROM vastai/comfy:v0.3.13-cuda-12.1-pytorch-2.5.1-py311

WORKDIR /workspace

COPY . .

RUN chmod +x start.sh comfyui.sh api.sh

ENTRYPOINT ["/workspace/start.sh"]