
#!/bin/sh

pwd
which python
which pip
python --version

pip install -r requirements.txt
uvicorn api:enroller --proxy-headers --host 0.0.0.0 --port 10000