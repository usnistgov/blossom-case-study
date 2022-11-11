FROM python:3.10-alpine

COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY requirements.txt /requirements.txt
COPY oscal_test.py /oscal_test.py
COPY oscal.py /oscal.py

RUN pip install -r requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]
