#!/bin/sh

pip --version
pip install -r requirements.txt

uvicorn app.api:enroller --proxy-headers --host 0.0.0.0 --port 10000
