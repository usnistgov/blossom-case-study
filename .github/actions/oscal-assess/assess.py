#!/usr/bin/env python3

import logging
from os import environ, path, PathLike
from pathlib import Path
from typing import NamedTuple, Union
from yaml import safe_load
from content import extract_import_ssp

logging.basicConfig()
logger = logging.getLogger('oscal_assess')
logger.setLevel(getattr(logging, str(environ.get('OSCAL_ASSESS_LOGLEVEL', 'DEBUG')).upper()))

ASSESSMENT_RESULT_TEMPLATE = f"{path.dirname(path.realpath(__file__))}/assessment_result.yaml.j2"

class AssessmentWorkflowContext(NamedTuple):
    ap: dict
    ap_path: Union[str, bytes, Path, PathLike]
    ar_path: Union[str, bytes, Path, PathLike]
    ar_template_path: Union[str, bytes, Path, PathLike]
    ssp: dict
    ssp_path: Union[str, bytes, Path, PathLike]

def create_context() -> AssessmentWorkflowContext:
    """Create execution context for runtime requirements of workflow.
    """
    try:
        ap_path = Path(environ.get('INPUT_ASSESSMENT_PLAN_PATH')) if Path(environ.get('INPUT_ASSESSMENT_PLAN_PATH')).exists() else None
        ar_path = Path(environ.get('INPUT_ASSESSMENT_RESULTS_PATH')) if Path('INPUT_ASSESSMENT_RESULTS_PATH').parent.exists() else None
        ar_template_path =  Path(ASSESSMENT_RESULT_TEMPLATE) if (Path(ASSESSMENT_RESULT_TEMPLATE).exists()) else None

        ap = load_yaml(ap_path)
        ssp_path = extract_import_ssp(ap)
        ssp = load_yaml(f"{ap_path.parent}/{ssp_path}")

    except Exception as err:
        logger.error('Context builder failed because env vars or template file incorrect')
        raise err

    return AssessmentWorkflowContext(ap, ap_path, ar_path, ar_template_path, ssp, ssp_path)

def load_yaml(path: Union[str, bytes, Path, PathLike]):
    """Load an OSCAL Assessment Plan YAML file.
    """
    try:
        return safe_load(open(path, 'r'))

    except Exception as err:
        logger.error('Cannot load AP YAML file')
        raise err

def generate_assessment_result():
    """Generate an OSCAL Assessment Result YAML file based upon the result of automated assessment tests.
    """
    pass

def handler():
    """Main entrypoint for assessment plan processing and assessment result generation.
    """
    try:
        return
    except Exception as err:
        logger.error('Runtime error in handler, exception below')
        logger.exception(err)

if __name__ == '__main__':
    context = create_context()
    print(context)
