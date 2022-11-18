# Pulled over from blossom-archive Dockerfile created by AJ.
# Current maven:3.8.6-openjdk-11-slim
ARG MAVEN_VERSION=sha256:bed43e35f3e5f013670d4d7d247612de5ac82355b0c58c244005c532dfe6a1d7

FROM maven@${MAVEN_VERSION} as builder

ARG OSCALCLI_ARCHIVE_URL=https://github.com/usnistgov/oscal-cli/releases/download/v0.1.1/cli-core-0.1.1-oscal-cli.zip

RUN apt-get update && \
    apt-get install unzip && \
    curl -L -o /tmp/cli.zip "${OSCALCLI_ARCHIVE_URL}" && \
    mkdir -p /tmp/oscal-cli && \
    unzip /tmp/cli.zip -d /tmp/oscal-cli && \
    chmod +x /tmp/oscal-cli/bin/oscal-cli

FROM maven@${MAVEN_VERSION} 

LABEL org.opencontainers.image.source=https://github.com/usnistgov/blossom

COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY --from=builder /tmp/oscal-cli /opt/oscal-cli

ENTRYPOINT ["/docker-entrypoint.sh"]
