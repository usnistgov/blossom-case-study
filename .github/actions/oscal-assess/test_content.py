import yaml
import jmespath
import pytest

from content import extract_ssp_params, extract_ap_resource, extract_ap_task_link_uuid, extract_associated_control, extract_ap_tasks

ssp = yaml.safe_load(open("../../../.oscal/ssp.yaml", "r"))
ap = yaml.safe_load(open("../../../.oscal/assessment-plan.yaml", "r"))

def test_extract_ssp_params():
    params = extract_ssp_params(ssp)

    assert len(params) == 1

def test_extract_ap_resource():
    resource = extract_ap_resource(ap, '31291ea5-13d7-44c6-aac6-bc61d9975ec5')

    assert resource.title == 'AC-8 In-App'
    assert resource.file == 'assessments/ac_8_inapp.py'
    assert resource.hash == '97428f53de57bb72e4647c5726794d3d2247da90f6a286d12150b1042dd9204c'

def test_extract_ap_resource_sad():
    # test unknown uuid
    with pytest.raises(Exception):
        extract_ap_resource(ap, 'invalid-fake-uuid')

def test_extract_ap_link_uuid():
    task = jmespath.search('"assessment-plan".tasks[*]', ap)[0]
    uuid = extract_ap_task_link_uuid(task)

    assert uuid == '31291ea5-13d7-44c6-aac6-bc61d9975ec5'

def test_extract_associated_control():
    assert extract_associated_control(ap, "d85636e6-0d9d-4c94-a924-5a612a119040") == 'ac-8'

def test_extract_ap_tasks():
    tasks = extract_ap_tasks(ap, ssp)

    assert len(tasks) == 1

    task = tasks[0]

    assert task.uuid == '6b7e6a29-4588-46be-b242-a0bda0092eec'
    assert task.title == 'Validate System Use Notification Presence from Python Script'

    # assert resources are carried over
    assert task.resource.title == 'AC-8 In-App'
    assert task.resource.file == 'assessments/ac_8_inapp.py'
    assert task.resource.hash == '97428f53de57bb72e4647c5726794d3d2247da90f6a286d12150b1042dd9204c'

    assert task.associated_control == 'ac-8'
    assert len(task.params) == 1
    assert 'ac-8_prm_1' in task.params

    assert len(task.props) == 2

    assert task.props['ar-check-method'] == 'system-shell-return-code'
    assert task.props['ar-check-result'] == '0'
