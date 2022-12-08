#!/usr/bin/env bash

set -Eeuo pipefail

/opt/oscal-cli/bin/oscal-cli $INPUT_MODEL_TYPE validate $INPUT_FILE_PATH
