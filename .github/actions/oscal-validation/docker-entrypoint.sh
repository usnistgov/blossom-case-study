#!/bin/sh -l

find .oscal -type f -name '*.yaml' -exec /opt/oscal-cli/bin/oscal-cli assessment-plan validate {} \;
