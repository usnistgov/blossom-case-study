import jmespath
from typing import Dict, NamedTuple, List

SET_PARAMS_PATH = (
    '"system-security-plan"."control-implementation"."implemented-requirements"[*]'
    '.{id: "control-id", params: "set-parameters"[*].{id: "param-id", values: "values"}}'
)

def extract_ssp_params(input_ssp: dict) -> Dict[str, Dict[str, str]]:
    '''
    Returns a nested dict of control_id -> (param_id -> values)
    Note that the values are flattened and joined with a '; '
    '''
    raw = jmespath.search(SET_PARAMS_PATH, input_ssp)
    return {
        impl_control['id']: {
            # 'values' is a list, for our purposes, just flatten it to a single string
            param['id']: '; '.join(param['values']) for param in impl_control['params']
        } for impl_control in raw
    }

class ApTaskResource(NamedTuple):
    uuid: str
    title: str
    description: str
    file: str
    hash: str

def extract_ap_resource(input_ap: dict, uuid: str) -> ApTaskResource:
    # TODO: probably sanitize this in a real world scenario?
    raw_resource = jmespath.search(f'''
        "assessment-plan"."back-matter".resources[?uuid==\'{uuid}\']
    ''', input_ap)

    if len(raw_resource) != 1:
        raise Exception(f'Resource with uuid "{uuid}" expected, but {len(raw_resource)} were found')
    raw_resource = raw_resource[0]

    if len(raw_resource['rlinks']) != 1:
        raise Exception('Resource with uuid "{}" expected to have one rlink, but {} were found'
            .format(uuid, len(raw_resource['rlinks'])))
    rlink = raw_resource['rlinks'][0]

    if len(rlink['hashes']) != 1:
        raise Exception('Resource with uuid "{}" expected to have an rlink with one hash, but {} were found'
            .format(uuid, len(rlink['hashes'])))
    hash = rlink['hashes'][0]['value']

    # TODO: support multiple hash algorithms

    return ApTaskResource(
        uuid=raw_resource['uuid'],
        title=raw_resource['title'],
        description=raw_resource['description'],
        file=rlink['href'],
        hash=hash
    )

class ApTask(NamedTuple):
    uuid: str
    title: str
    description: str
    resource: ApTaskResource
    params: Dict[str, str]
    associated_control: str
    # name -> value
    props: Dict[str, str]

def extract_ap_task_link_uuid(input_ap_task: dict) -> str:
    # grab the resource link for the task
        href = jmespath.search("links[?rel=='command'].href", input_ap_task)
        if len(href) != 1:
            raise Exception('Task (uuid={}) should only have one command link, got {}'
                    .format(input_ap_task['uuid'], len(href)))
        href = href[0]
        if not href.startswith('#'):
            raise Exception(f'Task link "{href}" is not a valid uuid link')

        return href[1:]

def extract_associated_control(input_ap: dict, uuid: str) -> str:
    return jmespath.search(f'"assessment-plan"."local-definitions"."activities"[?uuid==\'{uuid}\']."related-controls"[*]."control-selections"[0]', input_ap)[0][0]

def extract_ap_tasks(input_ap: dict, input_ssp: dict) -> List[ApTask]:
    raw_tasks = jmespath.search('"assessment-plan".tasks[?type==\'action\']', input_ap)

    ssp_params = extract_ssp_params(input_ssp)

    tasks = []
    for raw_task in raw_tasks:
        link_uuid = extract_ap_task_link_uuid(raw_task)
        resource = extract_ap_resource(input_ap, link_uuid)

        associated_control = extract_associated_control(input_ap, raw_task['associated-activities'][0]['activity-uuid'])
        params = ssp_params.get(associated_control, {})

        props = {
            prop['name']: prop['value']
            for prop in raw_task['props']
        }

        tasks.append(ApTask(
            uuid=raw_task['uuid'],
            title=raw_task['title'],
            description=raw_task['description'],
            resource=resource,
            params=params,
            associated_control=associated_control,
            props=props
        ))

    return tasks
