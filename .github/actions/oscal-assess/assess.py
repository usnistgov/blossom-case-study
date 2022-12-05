#!/usr/bin/env python3

from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging
from os import environ, path, PathLike
from pathlib import Path
import subprocess
from sys import exit
from typing import Dict, List, NamedTuple, Union
from uuid import uuid4
from yaml import safe_dump, safe_load

from content import ApTask, extract_ap_tasks, extract_import_ssp, extract_reviewed_controls

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
        ap_path = Path(environ.get('INPUT_ASSESSMENT_PLAN_PATH', 'nopath')) if Path(environ.get('INPUT_ASSESSMENT_PLAN_PATH', 'nopath')).exists() else None
        ar_path = Path(environ.get('INPUT_ASSESSMENT_RESULTS_PATH', 'nopath')) if Path(environ.get('INPUT_ASSESSMENT_RESULTS_PATH', 'nopath')).parent.exists() else None
        ar_template_path =  Path(ASSESSMENT_RESULT_TEMPLATE) if (Path(ASSESSMENT_RESULT_TEMPLATE).exists()) else None
        ar_template_file = ar_template_path.name

        if not ap_path: raise RuntimeError('Assessment plan path invalid')
        if not ar_path: raise RuntimeError('Assessment result output path invalid')
        if not ar_template_path: raise RuntimeError('Path for assessment template file invalid')

        ap = load_yaml(ap_path)
        ssp_file = extract_import_ssp(ap)
        ssp_path = Path(f"{ap_path.parent}/{ssp_file}") if Path(f"{ap_path.parent}/{ssp_file}").exists() else None

        if not ssp_path: raise RuntimeError('Invalid path for SSP file referenced in assessment plan path invalid')

        ssp = load_yaml(ssp_path)

        ar_renderer = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

        # By default, Jinja2 does not have a filter to convert Python objects
        # from Python to YAML, only JSON, we have to create our own filter.
        # https://github.com/kapicorp/kapitan/issues/27
        # https://github.com/kapicorp/kapitan/pull/32
        def jinja2_yaml_filter(obj):
            return safe_dump(obj, default_flow_style=False)

        ar_renderer.filters['to_yaml'] = jinja2_yaml_filter

        context = AssessmentWorkflowContext(
            ap, ap_path, 
            ar_path, ar_template_path, ar_template_file,
            ssp, ssp_path, 
            tasks_results=[], 
            ar_renderer=ar_renderer
        )

        logger.debug(f"Context: {context}")
        return context
        
    except Exception as err:
        logger.error('Context builder failed')
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
            task_result = run_task(t)
            context.tasks_results.append(ApTaskResult(t,task_result if type(task_result) == bool else False))

        except Exception as err:
            logger.exception(err)
            logger.error(f"Running task {idx+1} failed, continuing to next task if any")
            continue

def run_task(task: ApTask):
    """Execute an OSCAL Assessment Plan task with a ar-check-method as defined
    in the relevant property as one of type 'system-shell-return-code' and
    return a boolean that reflects whether the actual POSIX shell return code
    matches the expected return code value as defined in the value of the prop
    'ar-check-result' for that task.
    """
    try:
        logger.debug(f"Trying to run task '{task.title}' with uuid {task.uuid}")
        ar_check_method = task.props.get('ar-check-method', '')
        ar_check_result = int(task.props.get('ar-check-result'))

        if ar_check_method != 'system-shell-return-code':
            logger.warning(f"Task ar-check-method is unsupported '{ar_check_method}', not 'system-shell-return-code'")
            return False

        env = environ.copy()
        for raw_param, value in task.params.items():
            param = 'SSP_PARAM_' + raw_param.upper().replace('-', '_')
            env[param] = value

        task_res_path = Path(task.resource.file)
        return_code = subprocess.call(task_res_path, env=env)
        return return_code == ar_check_result

    except Exception as err:
        logger.error(f"Running task with uuid {task.uuid} failed")
        raise err

def tasks_results_to_observations(tasks_results: List[ApTaskResult], current_timestamp: str) -> dict:
    """Cross reference an Assessment Plan's activities, its tasks, their
    results and generate a dictionary of observation to be inserted in the
    Assessment Results template.
    """
    raw_data = {'observations': []}

    for tr in tasks_results:
        task = tr.task
        method = task.associated_activity_props.get('method')
        observation_uuid = str(uuid4())
        raw_data['observations'].append({
            'uuid': observation_uuid,
            'methods': [method],
            'title': task.title if task.title else f"OSCAL Assessment Workflow Observation {observation_uuid}",
            'description': task.description if task.description else 'No description provided',
            'props': [
                {
                    'name': 'assessment-plan-task-uuid',
                    'ns': 'https://www.nist.gov/itl/csd/ssag/blossom',
                    'value': task.uuid
                },
                {
                    'name': 'assessment-plan-task-result',
                    'ns': 'https://www.nist.gov/itl/csd/ssag/blossom',
                    'value': str(tr.result) if tr.result else 'False'
                }
            ],
            'relevant-evidence': [
                {
                    'href': 'https://example.com/path/to/scan',
                    'description': 'This observation is the result of automated testing in a run of a GitHub Actions workflow. For detailed information, please review the run status and detailed logging from its configuration, step inputs, and step outputs.'
                }
            ],
            'collected': current_timestamp
        })

    logger.debug(f"{len(raw_data.get('observations', {}))} observation(s) processed")
    return raw_data

def observations_to_findings(tasks_results: List[ApTaskResult], observations: List[dict]) -> dict:
    raw_data = {'findings': []}

    for o in observations:
        try:
            task_uuid = [prop for prop in o.get('props') if prop.get('name') == 'assessment-plan-task-uuid' and prop.get('ns') == 'https://www.nist.gov/itl/csd/ssag/blossom'][0].get('value')
            task_result = [prop for prop in o.get('props') if prop.get('name') == 'assessment-plan-task-result' and prop.get('ns') == 'https://www.nist.gov/itl/csd/ssag/blossom'][0].get('value')

            if not task_uuid or not task_result:
                logger.warn(f"Observation missed required assessment-plan-task-uuid and/or assesssment-plan-task-result props, skipping")
                continue
        
            if task_result != 'False':
                logger.debug(f"Task result for {task_uuid} for observation did not return false result, skipping")
                continue

            task = [tr.task for tr in tasks_results if tr.task and tr.task.uuid == task_uuid][0]

            objectives_count = len(task.associated_control_objective_selections)
            target_id = task.associated_control_objective_selections[0]

            if objectives_count > 1:
                logger.warn(f"Findings target one objective control selection, not multiple, selecting only {target_id}")
            
            finding_uuid = str(uuid4())
            raw_data['findings'].append({
                'uuid': finding_uuid,
                'title': f"Finding from Observation {o.get('uuid', 'ENOUUID')}",
                'description': task.description,
                'target': {
                    'type': 'objective-id',
                    'target-id': target_id,
                    'title': task.title,
                    'status': {
                        'state': 'not-satisfied',
                        'reason': 'failed'
                    }
                },
                'related-observations': [
                    {'observation-uuid': o.get('uuid', 'ENOUUID')}
                ]
            })

        except Exception as err:
            logger.error(f"Error in processing an observation, moving to next if found")
            logger.exception(err)

    logger.debug(f"{len(raw_data.get('findings', {}))} finding(s) processed from {len(observations)} observation(s).")
    return raw_data

def create_ar(context: AssessmentWorkflowContext):
    """Generate an OSCAL Assessment Result YAML file based upon the result of
    automated assessment tests.
    """
    try:
        current_timestamp = datetime.now(timezone.utc).isoformat()
        ap_reviewed_controls = extract_reviewed_controls(context.ap)
        ar_observations = tasks_results_to_observations(context.tasks_results, current_timestamp)
        ar_findings = observations_to_findings(context.tasks_results, ar_observations.get('observations', {}))

        with open(context.ar_path, 'w') as fh:
            template = context.ar_renderer.get_template(context.ar_template_file)
            ar = template.render({
                'ar_uuid': uuid4(),
                'ar_metadata_title': 'OSCAL Workflow Automated Assessment Results',
                'ar_metadata_last_modified_timestamp': current_timestamp,
                'ar_import_ap_href': f"./{context.ap_path.name}",
                'ap_reviewed_controls': ap_reviewed_controls,
                'ar_results_start_timestamp': current_timestamp,
                'ar_results_start_timestamp': current_timestamp,
                'ar_observations': ar_observations,
                # In OSCAL AR instances, we cannot have an empty findings: []
                # so we must trigger the template to insert a findings var at
                # at all for schema and constraint validation with oscal-cli.
                'ar_findings': ar_findings if len(ar_findings.get('findings')) > 0 else None
            })
            logger.debug(f"Writing rendered assessment result to {context.ar_path}")
            fh.write(ar)
            logger.info(f"Completed assessment per plan, wrote results to file")

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

        if not all([tr.result for tr in context.tasks_results]):
            logger.error(f"One or more automated tests failed, failing GitHub CI run")
            return exit(1)

        return exit(0)

    except Exception as err:
        logger.error('Runtime error in handler, exception below')
        logger.exception(err)

if __name__ == '__main__':
    handler()
