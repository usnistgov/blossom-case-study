# Pulled over from blossom-archive Dockerfile created by AJ.
# Current python:3-slim-buster
ARG PYTHON_VERSION=sha256:876053fd9c3f645ed21e9e03122ecc1520be76473be89e5d222c748cad432bde

FROM python@${PYTHON_VERSION} as builder

FROM python@${PYTHON_VERSION} 

LABEL org.opencontainers.image.source=https://github.com/usnistgov/blossom-case-study

RUN mkdir -p /opt/oscal-assess/

COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY assess.py /opt/oscal-assess/
COPY content.py /opt/oscal-assess/
COPY requirements.txt /opt/oscal-assess
COPY assessment_result.yaml.j2 /opt/oscal-assess/

RUN python3 -m pip install -r /opt/oscal-assess/requirements.txt 

ENTRYPOINT ["/docker-entrypoint.sh"]
