#%%
import yaml
import jmespath
from typing import Dict, NamedTuple, List

# %%

ssp = yaml.safe_load(open("../../../.oscal/ssp.yaml", "r"))
ap = yaml.safe_load(open("../../../.oscal/assessment-plan.yaml", "r"))

# %%

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

extract_ssp_params(ssp)

# %%

class ApTaskResource(NamedTuple):
    uuid: str
    title: str
    description: str
    file: str
    hash: str

def extract_ap_resource(input_ap: dict, uuid: str) -> ApTaskResource:
    # TODO: probably sanitize this in a real world scenario?
    raw_resource = jmespath.search(f'"assessment-plan"."back-matter".resources[?uuid==\'{uuid}\']', input_ap)

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

def extract_ap_tasks(input_ap: dict, input_ssp: dict) -> List[ApTask]:
    raw_tasks = jmespath.search('"assessment-plan".tasks[?type==\'action\']', input_ap)

    ssp_params = extract_ssp_params(input_ssp)

    tasks = []
    for raw_task in raw_tasks:
        # grab the resource link for the task
        href = jmespath.search("links[?rel=='command'].href", raw_task)
        if len(href) != 1:
            raise Exception('Task (uuid={}) should only have one command link, got {}'
                    .format(raw_task['uuid'], len(href)))
        href = href[0]
        if not href.startswith('#'):
            raise Exception(f'Task link "{href}" is not a valid uuid link')
        href = href[1:]

        resource = extract_ap_resource(input_ap, href)

        tasks.append(ApTask(
            uuid=raw_task['uuid'],
            title=raw_task['title'],
            description=raw_task['description'],
            resource=resource,
            params={} # ssp_params[''] # TODO: get associated control
        ))

    return tasks

extract_ap_tasks(ap, ssp)
