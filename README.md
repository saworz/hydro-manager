# MyHydro

Simple Django app for hydro system management

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Project Setup

### Install virtual environment

- To isolate the dependencies of this project, it's recommended to use a virtual environment.

On Linux/macOS:

```
python3 -m venv env
```
On Windows:
```
python -m venv env
```

### Clone repository
```
git clone https://github.com/saworz/hydro
```

### Install dependencies
```
cd hydro-manager
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### Create and setup PostgreSQL database:
```
createdb --username=postgres hydro
export DATABASE_URL=postgres://postgres:hydro@127.0.0.1:5432/hydro
```

### Apply migrations
```
python manage.py migrate
```

### Run server
```
python manage.py runserver
```
