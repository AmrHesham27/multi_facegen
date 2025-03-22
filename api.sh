#!/bin/bash

cd /workspace/api

pip install -r requirements.txt
pip install --upgrade "pydantic>=2.0"
pip install --upgrade "pydantic>=2.0"

uvicorn main:app --reload --host 0.0.0.0 --port 5000