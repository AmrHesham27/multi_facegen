#!/bin/bash

# Related to the base docker image
bash /opt/instance-tools/bin/entrypoint.sh &

# Setup the API
bash api.sh &

# Setup the ComfyUI
bash comfyui.sh &

# Wait for both services to finish
wait