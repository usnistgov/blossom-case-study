# Case Study Usage Instructions and Overview
## Usage

This repository has branches saved to show the progression of a web application being developed, security controls being implemented as documented, and automated assessment procedures developed alongside them. The branches listed below show the step-by-step progression.

- [`step_0` branch](https://github.com/usnistgov/blossom-case-study/tree/step_0): This branch is essentially empty, and contains only the `README.md` to get started.
- [`step_1` branch](https://github.com/usnistgov/blossom-case-study/tree/step_1): This branch contains the initial demo web application, written with Python and the Flask framework, with a simple interface. It includes unit and basic integration tests. Below are important files worth noting.
  - [`api.py`](https://github.com/usnistgov/blossom-case-study/blob/step_1/app/api.py): The web application backend
  - [`non_conforming.html`](https://github.com/usnistgov/blossom-case-study/blob/step_1/app/views/warning/non_conforming.html): A template for frontend markup configured to present a banner encouraging the user to enjoy their day
  - [`conforming.html`](https://github.com/usnistgov/blossom-case-study/blob/step_1/app/views/warning/conforming.html): A template for frontend markup configured to present a banner informing users they are using a government system and must consent to system monitoring
  - [`test_api.py`](https://github.com/usnistgov/blossom-case-study/blob/step_1/tests/test_api.py): A simple unit test, not testing security controls
  - [`ci.yaml`](https://github.com/usnistgov/blossom-case-study/blob/step_1/.github/workflows/ci.yaml): A basic GitHub Actions workflow that runs the unit tests (using the `pytest` framework)
- [`step_2` branch](https://github.com/usnistgov/blossom-case-study/tree/step_2): This branch adds security documentation and automated assessment procedures in the OSCAL YAML format. It also extends the CI workflows in GitHub Actions to run not only application unit tests, but also run automated assessments driven by the OSCAL YAML content. Below are important files worth noting.
  - [`profile.yaml`](https://github.com/usnistgov/blossom-case-study/blob/step_2/.oscal/profile.yaml): A profile, a declarative definition of OSCAL of how to tailor and scope controls from another catalog
  - [`resolved-catalog.yaml`](https://github.com/usnistgov/blossom-case-study/blob/step_2/.oscal/resolved-catalog.yaml): A catalog, the resulting tailored selection of modified controls
  - [`ssp.yaml`](https://github.com/usnistgov/blossom-case-study/blob/step_2/.oscal/ssp.yaml): A system security plan, the description of the system (here, the demo web application), its properties, its current deployment statement, the and security controls implemented in the system (if coded correctly, this one might have some errors)
  - [`assessment-plan.yaml`](https://github.com/usnistgov/blossom-case-study/blob/step_2/.oscal/assessment-plan.yaml): A plan of how one or more assessors and/or their automation platforms will test the system's for the soundness of security control implementation
  - [`ci.yaml`](https://github.com/usnistgov/blossom-case-study/blob/step_2/.github/workflows/ci.yaml): An updated GitHub Actions workflow that runs unit tests, but also validates OSCAL YAML content against the model schemas using the `oscal-validate` action. If validation passes, it will run the automated assessment procedures using the assessment plan using the `oscal-assess` action.
- [`step_3` branch](https://github.com/usnistgov/blossom-case-study/tree/step_3): This branch uses [the information from results a failure in CI workflow run](https://github.com/usnistgov/blossom-case-study/actions/runs/3643649707/jobs/6152082288) to correct errors in the demo app's system security plan in OSCAL YAML form. Below are important files worth noting.
  - [`ssp.yaml`](https://github.com/usnistgov/blossom-case-study/blob/step_3/.oscal/ssp.yaml): A system security plan that has been corrected to included missing data in the security control implementation section
- [`step_4` branch](https://github.com/usnistgov/blossom-case-study/tree/step_4): This branch uses [the information from results a failure in CI workflow run](https://github.com/usnistgov/blossom-case-study/actions/runs/3643653295/jobs/6152098658) to correct errors in the demo app's configuration based on a failed assessment result (which is [a generated output from the workflow run](https://github.com/usnistgov/blossom-case-study/suites/9734751500/artifacts/467089353) in OSCAL YAML format). Below are important files worth noting.
  - [`api.py`](https://github.com/usnistgov/blossom-case-study/blob/step_4/app/api.py): An updated version of the web application backend to successfully pass an assessment specified in the assessment plan

## Project Structure

### .github/

This directory contains the overall CI workflow for GitHub Actions, as well as the custom GitHub Actions to interpret OSCAL content.

### .oscal/

This directory contains OSCAL model files.

### app/

This directory contains the target application to be tested and assessed.  This would typically be the application being developed.

### assessments/

This directory contains test script(s) for security control objectives that are automatable. In this project, they are executed as a part of [the assessment action, `oscal-assess`](.github/actions/oscal-assess) in the workflow.


### cypress/

This directory contains user acceptance tests, which could also include testing of controls.  Cypress can produce evidence through screenshots and videos to demonstrate more complex use case scenarios for one or more controls.

### tests/

This directory contains test that would be a part of the standard unit/regression tests for the application being developed.



## Implemented Workflow

![General Concept](diagrams/Concept.drawio.svg)




