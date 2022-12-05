# Case Study Usage Instructions and Overview
## Usage



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




