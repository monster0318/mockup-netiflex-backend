<p style="font-family: system-ui, sans-serif;font-size:40px; font-weight:700">
VIDEOFLIX API DOCUMENTATION
</p>

## Table of Contents

1. [Project Setup](#project-setup)
2. [Endpoints Overview](#endpoints-overview)
3. [Swagger OpenAPI Documentation](#swagger-openapi-documentation)
4. [Unit Testing](#unit-testing)
   4.1. [Running Testcases](#running-testcases)
   4.2. [Coverage Report](#coverage-report)
5. [Celery and Redis Task Queuing and Scheduling](#task-scheduling)
6. [Periodic Data Import Export](#db-export)

All the packages use in the projects are listed in the requirement.txt data with their corresponding version. The next lines show how to set up an environment to run the project.

---

## 1. Project Setup

#### 1.1. Create a virtual environment (venv)

    python -m venv <name_of_the_virtual_env> (for Windows users)
    python3 -m venv <name_of_the_virtual_env> (for MAC or Linux users)
    e.x. : python -m venv env

#### 1.2. Activate the venv

    .\<name_of_env>\Scripts\activate  (for Windows users)
    source <name_of_env>/bin/activate (for MAC or Linux users)

#### 1.3. Install packages from requirements.txt

    pip install -r requirements.txt

#### 1.4. Run migration

    python manage.py makemigrations user authentication videoflix_app
    python manage.py migrate

#### 1.5. Start celery worker process for task queuing

If you want to upload new video to the backend, it will be a good idea to start <a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">celery</a> worker, which uses <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> as broker, for queuing heavy task in the background while you can continue with other tasks. Celery and django celery beat are documented in section 5.

    celery -A videoflix worker -l INFO

#### 1.5. Run the development server

    python manage.py runserver

## 3. Swagger OpenAPI Documentation

The videoflix API was documented using the openAPI standard with swagger-ui. This allow a browsable testing view of the API like the rest framework does but with more sophisticated and customizable UI. The Swagger UI can be access though the following link:

<a href="http://localhost:8000/swagger/" target="_blank">OpenAPI-Swagger-ui</a>
