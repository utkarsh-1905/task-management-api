## Project Task Management API

![Testing Workflow](https://github.com/utkarsh-1905/task-management-api/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/utkarsh-1905/task-management-api/graph/badge.svg?token=2CR8DKPIFO)](https://codecov.io/gh/utkarsh-1905/task-management-api)

**View the [Test Results](https://utkarsh-1905.github.io/task-management-api/report.html) here.**

---

### Assumptions

- Project Owner cannot be changed
- Any user can create a Task for a project regardless of whether they are a owner of the project or not (same as Github/OSS project)
- Task can be assigned to any user/self by owner/admin
- Task can be reviewed by multiple users/self and assigned by owner/admin
- Tasks and Projects can be read by all but can be updated/deleted only by the object owner/admin
- Currently, all users can be seen using a get request but in production, this should be prohibited due to security and privacy concerns

### Features

- Create, Read, Update and Delete Projects
- Create, Read, Update and Delete Tasks
- Assign Tasks to Users
- Add reviewers to tasks
- Unit, Integration and E2E tests for the API
- Custom Model Factories for testing
- Github action to run all test cases and host the test report on github pages
- Dockerfile to run the project in a container
- Swagger UI documentation for the API
- Custom permissions for the API

### Running the project

#### Using Docker

- Clone the project using `git clone https://github.com/utkarsh-1905/task-management-api.git`
- Run `docker build -t task-management-api .`
- Run `docker run -p 8000:8000 --name tm-api task-management-api`

#### Using Python

- Clone the project
- Create a virtual environment
- Run `pip install -r requirements.txt`
- Run `python manage.py makemigrations && python manage.py migrate` or `make migrate`
- Run `python manage.py runserver` or `make run`
- Run `python manage.py test` or `make test` to run all the test cases (unit, integration and e2e)

### Testing (98 Test Cases)

- The project uses `pytest` for testing
- The project uses `pytest-cov` for coverage
- The `tests/` directory contains all the test cases
- Folders with app names, contains and unit and integration tests
- The model and serializer tests contain the unit tests
- The view tests contain the integration tests
- The `e2e/` directory contains the end to end tests of the api

### API Documentation

- Get the Swagger api documentaion at `/docs/`
- [Postman Documentation](https://documenter.getpostman.com/view/17651518/2s9YC31tdY)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/17651518-2192945c-4292-4129-89a4-b00b692d06ba?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D17651518-2192945c-4292-4129-89a4-b00b692d06ba%26entityType%3Dcollection%26workspaceId%3D844f7943-5de7-4b14-9ff1-a909d2d47181)

**To make the response timezone aware, include time_zone='your time zone' query parameter in GET request.** [Refer to list of all timezones.](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)

### Difficulties Faced

- Creating Model factories to test data
- Setting up custom permissions
- Excluding test dependencies in Dockerfile
