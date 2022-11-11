import os, yaml
from pathlib import Path
from yaml import load


if 'ASSESSMENT_PLAN' not in os.environ:
    exit("Assessment Plan Environment Variable Not Found")


model = os.environ['ASSESSMENT_PLAN']


def test_the_load():
    """Load a model for interpretation"""
    content = Path(model).read_text()
    plan = yaml.safe_load(content)

    print("*"*100)
    print(model)
    print(plan)

# These should be tests to test oscal.py for issues.
# If this fails, then oscal.py should not run.
def test_to_pass():
    """Passing Test"""
    assert True == True