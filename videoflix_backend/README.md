<p style="font-family: system-ui, sans-serif;font-size:40px; font-weight:700">
VIDEOFLIX API DOCUMENTATION
</p>

## Table of Contents

1. [Project Setup](#project-setup)
2. [Endpoints Overview](#endpoints-overview)
3. [Swagger OpenAPI Documentation](#swagger-openapi-documentation)
   3.1. [Redoc Documentation](#redoc-documentation)
   3.2. [Testing the API with swagger UI](#swagger-ui-testing)
4. [Unit Testing](#unit-testing)
   4.1. [Running Testcases](#running-testcases)
   4.2. [Coverage Report](#coverage-report)
5. [Celery and Redis: Caching, Task Queuing and Scheduling](#task-scheduling)
6. [Periodic Data Import Export](#db-export)
   6.1. [Exporting DB Data manually](#manual-export)
   6.2. [Exporting DB Data periodically](#periodic-export)

All the packages use in the projects are listed in the requirement.txt data with their corresponding version. For a brief summary: The videoflix API allow authentication through the authentication endpoints. Users can register but will have to activate their account after registration. The activation link is sent per email to the user. After activation of the account the user can login with his credentials. If the login is successful then the user will have access to the videos of the platform. A demo login is also possible. The next lines show how to set up an environment to run the project and the services allowed.

---

## 1. Project Setup

#### 1.1. Create a virtual environment (venv)

    python -m venv <name_of_the_virtual_env>  (for Windows users)
    python3 -m venv <name_of_the_virtual_env> (for MAC or Linux users)
    e.x. : python -m venv env

#### 1.2. Activate the venv

    .\<name_of_env>\Scripts\activate  (for Windows users)
    source <name_of_env>/bin/activate (for MAC or Linux users)

#### 1.3. Install packages from requirements.txt

    pip install -r requirements.txt

#### 1.4. Run migration

<h6>For Windows users:</h6>

    python manage.py makemigrations user authentication videoflix_app
    python manage.py migrate

<h6>For MAC or Linux users:</h6>

    python3 manage.py makemigrations user authentication videoflix_app
    python3 manage.py migrate

#### 1.5. Start celery worker process for task queuing

If you want to upload new video to the backend, it will be a good idea to start <a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">celery</a> worker, which uses <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> as broker, for queuing heavy task in the background while you can continue with other tasks. Celery and django celery beat are documented in section 5.

    celery -A videoflix worker -l INFO

#### 1.5. Run the development server

    python manage.py runserver (for Windows users)
    python3 manage.py runserver (for MAC or Linux users)

## 2. Endpoints Overview

Since the endpoints are fully documented with OpenAPI specification, no further in-depth details will be given in this section. Visit the two links below after running your server to consult the documentation.

    http://localhost:8000/redoc/

## 3. Swagger OpenAPI Documentation

The videoflix API was documented using the openAPI standard with swagger-ui. This allow a browsable testing view of the API like the rest framework does but with more sophisticated and customizable UI. The OpenAPI documentation can be access via the "redoc/" endpoint and the Swagger UI endpoint "swagger/" can be used to test the API and interact with the available routes.
You can read the documentation or test the API through the following urls if you are using the development server and serve to the port 8000. Feel free to update the domain and the port number with your own domain (e.x.: <a>https://you_domain_name.com/<endpoint_name></a>).

#### 3.1 Redoc Documentation

    http://localhost:8000/redoc/

<img src="media/documentation/redoc.png" width="700">

#### 3.2 Testing the API with swagger UI

    http://localhost:8000/swagger/

## 4. Unit Testing

The API develop using the Test Driven Development TDD principle and modules have been tested with <a href="https://docs.python.org/3/library/unittest.html" target="_blank">unittest</a> by means of factory data from the factory boy library.

#### 4.1. Running Testcases

The test runner used in this project is <a href="https://docs.pytest.org/en/stable/contents.html" target="_blank">pytest</a>. Use the following command to run the unit test:

     python manage.py videoflix_tests (for Windows users)
     python3 manage.py videoflix_tests (for MAC or Linux users)

#### 4.2. Coverage Report

The test report shows that the code is 81 % covered by the unit test. The report with missing line can be seen in the following table.

<h6>Coverage HTML Report</h6>

Generated at: [`coverage_html_report/`](coverage_html_report/index.html)

You can also copy and paste this to your browser after running the server (update the domain and port number if necessary)

    http://localhost:8000/coverage_html_report/index.html

![Coverage](https://img.shields.io/badge/Coverage-81%25-brightgreen?style=flat-square)

| Name                              | Stmts | Miss | Cover   | Missing                                                                                         |
| --------------------------------- | ----- | ---- | ------- | ----------------------------------------------------------------------------------------------- |
| authentication/api/serializers.py | 129   | 2    | 98%     | 145-146                                                                                         |
| authentication/api/signals.py     | 23    | 0    | 100%    | -                                                                                               |
| authentication/api/utils.py       | 36    | 4    | 89%     | 55-63                                                                                           |
| authentication/api/views.py       | 78    | 0    | 100%    | -                                                                                               |
| authentication/models.py          | 1     | 0    | 100%    | -                                                                                               |
| fixtures/factories.py             | 64    | 0    | 100%    | -                                                                                               |
| user/api/forms.py                 | 6     | 6    | 0%      | 1-10                                                                                            |
| user/api/serializers.py           | 6     | 0    | 100%    | -                                                                                               |
| user/models.py                    | 36    | 3    | 92%     | 9, 26, 28                                                                                       |
| videoflix/celery.py               | 14    | 0    | 100%    | -                                                                                               |
| videoflix_app/api/filters.py      | 13    | 0    | 100%    | -                                                                                               |
| videoflix_app/api/paginations.py  | 4     | 4    | 0%      | 1-6                                                                                             |
| videoflix_app/api/permissions.py  | 10    | 1    | 90%     | 16                                                                                              |
| videoflix_app/api/serializers.py  | 12    | 0    | 100%    | -                                                                                               |
| videoflix_app/api/signals.py      | 25    | 0    | 100%    | -                                                                                               |
| videoflix_app/api/tasks.py        | 156   | 115  | 26%     | 21-25, 29-43, 64-92, 96-108, 112-126, 130-155, 166, 176-178, 182-195, 200-207, 212-236, 242-244 |
| videoflix_app/api/throttles.py    | 5     | 0    | 100%    | -                                                                                               |
| videoflix_app/api/utils.py        | 39    | 0    | 100%    | -                                                                                               |
| videoflix_app/api/views.py        | 56    | 7    | 88%     | 63-77                                                                                           |
| videoflix_app/models.py           | 26    | 0    | 100%    | -                                                                                               |
| **TOTAL**                         | 739   | 142  | **81%** | -                                                                                               |

## 5. Celery and Redis: Caching, Task Queuing and Scheduling

For requests optimization to the endpoint, <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> was used to cache request data every 15 minutes since the data are not intended to be changed very often.
<a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">Celery</a> and <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a>

## 6. Periodic Data Import Export

The Data can be exported either manually or let be exported by our tasks runner: <a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">celery worker</a>

#### 6.1 Exporting DB Data manually

The manual export can be achieve by running the following command in the terminal:

    python manage.py export_video_data (for Windows users)
    python3 manage.py export_video_data (for MAC or Linux users)

#### 6.2 Exporting DB Data periodically

To avoid a possible loss of data when the server is broken the database is periodically exported as json file. This export has been scheduled using django celery beat which send the task to celery worker that in turn uses its broker (here <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a>) for running the task in the background every Sunday at 6AM.
For this purpose the django celery beat service should also be started the same way we did with celery(please make sure <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> is also running and update the password of redis in settings.py). The command to start django celery beat service is as follow:

    celery -A videoflix beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

In production this need to be done by the daemon of your system, for instance systemd. However, the periodic tasks will be set up when celery worker starts and do not need to be done manually in the admin panel. Visit the admin panel to see the setting under Crontab.
