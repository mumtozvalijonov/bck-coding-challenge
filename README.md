# Interview Test Project
Given a polygon and a plane the RESTful API must return the cut result.

## Setup & Run
### Docker
#### Prerequisites
* Docker
* Docker Compose
* Make
```console
$ make docker
```

### Host machine
#### Prerequisites
* Python 3.7+
* Python-venv
* Make
```console
$ python3 -m venv venv
$ source venv/bin/activate
$ make setup
$ make run
```

## API Documentation
### Swagger
Navigate to `http://{host}:8000/docs` to view the Swagger documentation.
