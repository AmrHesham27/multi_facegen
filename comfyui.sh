#!/bin/bash

# Download packages

pip install tqdm packaging insightface onnxruntime
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install comfyui nodes

cd /workspace/ComfyUI/custom_nodes
git clone https://github.com/twri/sdxl_prompt_styler
git clone https://github.com/tsogzark/ComfyUI-load-image-from-url
git clone https://github.com/Gourieff/ComfyUI-ReActor
cd ..
python -m pip install -U pip
cd /workspace/ComfyUI/custom_nodes/ComfyUI-ReActor
python install.py
