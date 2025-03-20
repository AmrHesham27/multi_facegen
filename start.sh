#!/bin/bash

bash api.sh &

# Setup the ComfyUI
bash comfyui.sh &

# Wait for both services to finish
wait