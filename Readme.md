## Project Task Management API

![Testing Workflow](https://github.com/utkarsh-1905/task-management-api/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/utkarsh-1905/task-management-api/graph/badge.svg?token=2CR8DKPIFO)](https://codecov.io/gh/utkarsh-1905/task-management-api)

**View the [Test Results](https://utkarsh-1905.github.io/task-management-api/report.html) here.**

---

### Assumptions

- Project Owner cannot be changed
- Any user can create a Task for a project regardless of whether they are a owner of the project or not (same as Github/OSS project)
- Task can be assigned to any user by owner
- Task can be reviewed by multiple users and assigned by owner
- Tasks and Projects can be read by all but can be updated/deleted only by the object owner

### Running the project

#### Using Makefile

- Clone the project
- Create a virtual environment
- Install the requirements
- Run `make` to start the server

### Versions

- Django = 4.2.4
- DRF = 3.14.0
- Python = 3.11.5
