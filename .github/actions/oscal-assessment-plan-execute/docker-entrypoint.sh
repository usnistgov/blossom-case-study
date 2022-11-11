#!/bin/sh -l

# chmod +x run.sh

model=$1
echo "::set-output name=model::$model"

time=$(date)
echo "::set-output name=time::$time"

location=$(pwd)
echo "::set-output name=location::$location"


cat $model

python --version
pytest --version

export ASSESSMENT_PLAN=$model
pytest /oscal_test.py
python /oscal.py