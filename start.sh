#!/bin/bash

# Setup the API
bash api.sh &

# Setup the ComfyUI
bash comfyui.sh &

# Wait for both services to finish
wait