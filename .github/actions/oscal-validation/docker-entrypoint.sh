#!/bin/sh -l

# chmod +x docker-entrypoint.sh

models=$1
echo "::set-output name=model::$model"

time=$(date)
echo "::set-output name=time::$time"

location=$(pwd)
echo "::set-output name=location::$location"

cat $models

# /bin/bash ghcr.io/usnistgov/blossom/oscal-cli:0.1.0 -c "/opt/oscal-cli/bin/oscal-cli profile resolve --as=json --to=json --quiet /app/docs/rmf_lifecycle/system-security-plans/nist-moderate-example-profile.oscal.json > /app/docs/rmf_lifecycle/catalogs/nist-moderate-example-resolved_catalog.oscal.json 2>/dev/null"

# /opt/oscal-cli/bin/oscal-cli profile resolve --as=json --to=json --quiet /app/*/rmf_lifecycle/system-security-plans/nist-moderate-example-profile.oscal.json"
ls -ltra

echo "Validating SSPs"
find .oscal/**/ -type f -name '*.yaml' -exec /opt/oscal-cli/bin/oscal-cli assessment-plan validate {} \;
