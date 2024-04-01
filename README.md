# MyHydro

Simple Django app for hydro systems management. \
Contains features such as user authorization and authentication, CRUD operations for hydro systems, sensors and measurements. \
Views are tested in test_views dirs. App is also packed into docker network. \
Each user can manage one's systems (add them, update info, delete, read details). After creating system, one can add sensors to it.
After setting up sensors use "new-measurement" endpoint to add values read by them to PostgreSQL db. \
Api documentation is available at http://localhost:8000/api/docs/ \
Follow README to set up and use the app properly.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

# 1) Project Setup

### 1.1) Install virtual environment

- To isolate the dependencies of this project, it's recommended to use a virtual environment.

```
python -m venv .venv
.venv/Scripts/activate
```

### 1.2) Clone repository
```
git clone https://github.com/saworz/hydro
```

### 1.3) Install dependencies (or go to 1.7 and use docker)
```
cd hydro
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### 1.4) Create and setup PostgreSQL database:
```
createdb --username=postgres hydro
export DATABASE_URL=postgres://postgres:hydro@127.0.0.1:5432/hydro
```

### 1.5) Apply migrations
```
python manage.py migrate
```

### 1.6) Run server
```
python manage.py runserver
```

--------------

###  1.7) Or just run it in docker network
```
cd hydro
docker-compose up
```

## 2) User setup
### 2.1) Register new user
![user-register-image](https://github.com/saworz/images/blob/main/register.png?raw=true)

## 2.2) Login into existing account
- First you need to setup csrf global var. Tokens are passed as cookies automatically.
![csrf-setup-image](https://github.com/saworz/images/blob/main/csrf-setup.png?raw=true)
- And now you can log in.
![user-login-image](https://github.com/saworz/images/blob/main/login.png?raw=true)


## 3) Project workflow

### 3.1) Populatedb for quick start! (or go to 3.2 and do everything manually)
- To avoid setting up user, systems, sensors, measurements manually you can run this command and enjoy some dummy data.

```
python manage.py populatedb
```
- Now you can investigate the data in database or using GET endpoints described in api schema (step 3.5).


### 3.2) Create new system
### Let's say you just finished building new system that contains only 1 ph sensor and 1 temperature sensor and you want to save its measurements.
### Note: remember to add csrf token to headers:
![csrf-token-image](https://github.com/saworz/images/blob/main/csrf-token.png?raw=true)

- Now you can make system create request
![create-system-image](https://github.com/saworz/images/blob/main/create-system.png?raw=true)

### 3.3) Add sensors
- Now make two requests to create two sensors for this system
![add-sensor-image](https://github.com/saworz/images/blob/main/create-sensor.png?raw=true)
![add-sensor2-image](https://github.com/saworz/images/blob/main/create-sensor2.png?raw=true)

### 3.4) From now on measurements can be saved in the database using new-measurement endpoint
- Let's add sample measurements for both of sensors
![add-measurement-image](https://github.com/saworz/images/blob/main/measurement-1.png?raw=true)
![add-measurement2-image](https://github.com/saworz/images/blob/main/measurement-2.png?raw=true)

### 3.5) Now you can go back to system details and check last 10 measurements
![read-details-image](https://github.com/saworz/images/blob/main/system-details.png?raw=true)

### 3.6) There are also some other endpoints for updating or reading your systems and sensors
--------------
## 3) Tests
### To run tests execute
```
pytest
```
