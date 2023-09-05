## Project Task Management API

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
