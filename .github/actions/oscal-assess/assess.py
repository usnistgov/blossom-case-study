#!/usr/bin/env python3

from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging
from os import environ, path, PathLike
from pathlib import Path
import subprocess
from typing import Dict, List, NamedTuple, Union
from uuid import uuid4
from yaml import safe_load

from content import ApTask, extract_ap_tasks, extract_import_ssp

logging.basicConfig()
logger = logging.getLogger('oscal_assess')
logger.setLevel(getattr(logging, str(environ.get('OSCAL_ASSESS_LOGLEVEL', 'DEBUG')).upper()))

SCRIPT_DIR = path.dirname(path.realpath(__file__))
TEMPLATES_DIR = f"{SCRIPT_DIR}/templates"
ASSESSMENT_RESULT_TEMPLATE = f"{TEMPLATES_DIR}/assessment_result.yaml.j2"

class ApTaskResult(NamedTuple):
    task: ApTask
    result: bool

class AssessmentWorkflowContext(NamedTuple):
    ap: dict
    ap_path: Union[str, bytes, Path, PathLike]
    ar_path: Union[str, bytes, Path, PathLike]
    ar_template_path: Union[str, bytes, Path, PathLike]
    ar_template_file: str
    ssp: dict
    ssp_path: Union[str, bytes, Path, PathLike]
    tasks_results: List[ApTaskResult]
    ar_renderer: Environment

def create_context() -> AssessmentWorkflowContext:
    """Create execution context for runtime requirements of workflow.
    """
    try:
        ap_path = Path(environ.get('INPUT_ASSESSMENT_PLAN_PATH')) if Path(environ.get('INPUT_ASSESSMENT_PLAN_PATH')).exists() else None
        ar_path = Path(environ.get('INPUT_ASSESSMENT_RESULTS_PATH')) if Path('INPUT_ASSESSMENT_RESULTS_PATH').parent.exists() else None
        ar_template_path =  Path(ASSESSMENT_RESULT_TEMPLATE) if (Path(ASSESSMENT_RESULT_TEMPLATE).exists()) else None
        ar_template_file = ar_template_path.name

        ap = load_yaml(ap_path)
        ssp_path = extract_import_ssp(ap)
        ssp = load_yaml(f"{ap_path.parent}/{ssp_path}")

        return AssessmentWorkflowContext(
            ap, ap_path, 
            ar_path, ar_template_path, ar_template_file,
            ssp, ssp_path, 
            tasks_results=[], 
            ar_renderer=Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        )
        
    except Exception as err:
        logger.error('Context builder failed because env vars or template file incorrect')
        raise err

def load_yaml(path: Union[str, bytes, Path, PathLike]):
    """Load an OSCAL Assessment Plan YAML file.
    """
    try:
        return safe_load(open(path, 'r'))

    except Exception as err:
        logger.error('Cannot load AP YAML file')
        raise err

def process_ap(context):
    """Process the OSCAL Assessment Plan to retrieve tasks, execute them, and
    return results to be inserted into OSCAL Assessment Results doc template.
    """
    # Extract automation tasks from the assessment plan.
    tasks = extract_ap_tasks(context.ap, context.ssp)
    tasks_count = len(tasks)
    logger.debug(f"Processed {context.ap_path} and found {tasks_count} tasks to run")

    for idx, t in enumerate(tasks):
        try:
            logger.debug(f"Running task {idx+1}/{tasks_count}")
            task_result = ApTaskResult
            context.tasks_results.append(ApTaskResult(t,task_result if type(task_result) == bool else False))

        except Exception as err:
            logger.exception(err)
            logger.err(f"Running task {idx+1} failed, continuing to next task if any")
            continue

def run_task(task: ApTask):
    try:
        logger.debug(f"Trying to run task '{task.title}' with uuid {task.uuid}")
        ar_check_method = task.props.get('ar-check-method', '')
        ar_check_result = int(task.props.get('ar-check-result'))

        if ar_check_method != 'system-shell-return-code':
            logger.warning(f"Task ar-check-method is unsupported '{ar_check_method}', not 'system-shell-return-code'")
            return False

        env = environ.copy()
        for raw_param, value in task.params:
            param = 'SSP_PARAM_' + raw_param.capitalize().replace('-', '_')
            env[param] = value

        task_res_path = Path(task.resource.file)
        return_code = subprocess.call(task_res_path, env=env)
        return return_code == ar_check_result

    except Exception as err:
        logger.error(f"Running task with uuid {task.uuid} failed")
        raise err

def create_ar(context: AssessmentWorkflowContext):
    """Generate an OSCAL Assessment Result YAML file based upon the result of automated assessment tests.
    """
    try:
        current_timestamp = datetime.now(timezone.utc).isoformat()

        with open(context.ar_path, 'w') as fh:
            template = context.ar_renderer.get_template(context.ar_template_file)
            ar = template.render({
                'ar_uuid':uuid4(),
                'ar_metadata_title': 'OSCAL Workflow Automated Assessment Results',
                'ar_metadata_last_modified_timestamp': current_timestamp,
                'ar_import_ap_href': f"./{context.ap_path.name}",
                'ar_results_start_timestamp': current_timestamp
            })
            logger.debug(f"Writing rendered assessment result to {context.ar_path}")
            fh.write(ar)

    except Exception as err:
        logger.error(f"Rending assessment result with {context.ar_template_path} failed")
        raise err

def handler():
    """Main entrypoint for assessment plan processing and assessment result generation.
    """
    try:
        logger.info(f'OSCAL Assessment Workflow started')
        logger.debug('Building OSCAL Assessment Workflow context')
        context = create_context()
        logger.debug('Processing assessment plan and executing automated tasks')
        process_ap(context)
        logger.debug('Generating assessment results from template and saving file')
        create_ar(context)
        logger.info(f'OSCAL Assessment Workflow ended')
    except Exception as err:
        logger.error('Runtime error in handler, exception below')
        logger.exception(err)

if __name__ == '__main__':
    handler()
