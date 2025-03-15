<p style="font-family: system-ui, sans-serif;font-size:40px; font-weight:700">
VIDEOFLIX API DOCUMENTATION
</p>

## Table of Contents

1. [Prerequisites]
2. [Project Setup](#project-setup)
3. [Endpoints Overview](#endpoints-overview)
4. [Swagger OpenAPI Documentation](#swagger-openapi-documentation)
   4.1. [Redoc Documentation](#redoc-documentation)
   4.2. [Testing the API with swagger UI](#swagger-ui-testing)
5. [Unit Testing](#unit-testing)
   5.1. [Running Testcases](#running-testcases)
   5.2. [Coverage Report](#coverage-report)
6. [Celery and Redis: Caching, Task Queuing and Scheduling](#task-scheduling)
7. [Periodic Data Import Export](#db-export)
   7.1. [Exporting DB Data manually](#manual-export)
   7.2. [Exporting DB Data periodically](#periodic-export)

All the packages use in the projects are listed in the requirement.txt data with their corresponding version. For a brief summary: The videoflix API allow authentication through the authentication endpoints. Users can register but will have to activate their account after registration. The activation link is sent per email to the user. After activation of the account the user can login with his credentials. If the login is successful then the user will have access to the videos of the platform. A demo login is also possible. The next lines show how to set up an environment to run the project and the services allowed.

---

## 1. Prerequisites

Before running the project, ensure you have the following dependencies installed:

### FFmpeg Installation

FFmpeg is required for handling video processing tasks.

- **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html#build-windows) and follow [this installation guide](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)
- **Mac**: Install via Homebrew:

```sh
brew install ffmpeg
```

- **Linux**: Install via package manager:

```sh
sudo apt update && sudo apt install ffmpeg
```

### Redis Installation

- **Windows**: [Download Redis](https://github.com/tporadowski/redis) and follow [this installation guide](https://github.com/tporadowski/redis)
- **Mac**: Install via Homebrew:

```sh
brew install redis
```

- **Linux**: Install via package manager:

```sh
sudo apt update && sudo apt install redis-server
```

### PostgreSQL 16 Installation

- **Windows**: [Download and Install PostgreSQL](https://www.postgresql.org/download/windows/)
- **Mac**: Install via Homebrew:

```sh
brew install postgresql@16
```

- **Linux**: Install via package manager:

```sh
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt install postgresql-16
```

### Verify Installations

After installation, confirm everything is installed correctly:

```sh
ffmpeg -version
redis-server --version
psql --version
```

If everything have successfully been installed:

## Access PostgreSQL as the postgres User

```sh
sudo psql -U postgres
```

## Change the Password for postgres

```sh
ALTER USER postgres WITH PASSWORD 'your_password';
```

## Create a New Database

```sh
CREATE DATABASE your_database_name;
```

## Exit PostgreSQL

```sh
\q
```

## Configuration Parameters

Navigate to the folder <b>/config</b> and open the file <b>config_settings.py</b> Replace the following parameters with your data:

Please set ups all the password otherwise you will need to make changes in settings.py to run the project.

```sh
SQL_USER="postgres"
SQL_PWD=""  # Password of your postgreSQL
RQ_PWD = "" # Password of redis you installed
MAIL_USERNAME="" # email of the user for smtp email connection
MAIL_PASSWORD="" # App password of the email for authentication
ADMIN_NAME = "" # username of the admin created on the console with createsuperuser command
EMAIL_HOST="smtp.gmail.com"
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
DB_NAME="" # name of database created in postgreSQL
DB_HOST="127.0.0.1"
DOMAIN_PROD = "" (optional, only necessary for production) # domain of the app in production

```

## 2. Project Setup

#### 2.1. Create a virtual environment (venv)

    python -m venv <name_of_the_virtual_env>  (for Windows users)
    python3 -m venv <name_of_the_virtual_env> (for MAC or Linux users)
    e.x. : python -m venv env

#### 2.2. Activate the venv

    .\<name_of_env>\Scripts\activate  (for Windows users)
    source <name_of_env>/bin/activate (for MAC or Linux users)

#### 2.3. Install packages from requirements.txt

    pip install -r requirements.txt

#### 2.4. Run migration

<h6>For Windows users:</h6>

    python manage.py makemigrations user authentication videoflix_app
    python manage.py migrate

<h6>For MAC or Linux users:</h6>

    python3 manage.py makemigrations user authentication videoflix_app
    python3 manage.py migrate

#### 2.5. Start celery worker process for task queuing

If you want to upload new video to the backend, it will be a good idea to start <a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">celery</a> worker, which uses <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> as broker, for queuing heavy task in the background while you can continue with other tasks. Celery and django celery beat are documented in section 5.

    celery -A videoflix worker -l INFO

#### 2.6. Run the development server

    python manage.py runserver (for Windows users)
    python3 manage.py runserver (for MAC or Linux users)

## 3. Endpoints Overview

Since the endpoints are fully documented with OpenAPI specification, no further in-depth details will be given in this section. Visit the two links below after running your server to consult the documentation.

    http://localhost:8000/redoc/

## 4. Swagger OpenAPI Documentation

The videoflix API was documented using the openAPI standard with swagger-ui. This allow a browsable testing view of the API like the rest framework does but with more sophisticated and customizable UI. The OpenAPI documentation can be access via the "redoc/" endpoint and the Swagger UI endpoint "swagger/" can be used to test the API and interact with the available routes.
You can read the documentation or test the API through the following urls if you are using the development server and serve to the port 8000. Feel free to update the domain and the port number with your own domain (e.x.: <a>https://you_domain_name.com/<endpoint_name></a>).

#### 4.1 Redoc Documentation

    http://localhost:8000/redoc/

<img src="https://github.com/user-attachments/assets/e95e6cfc-bf4b-47b6-9b89-6c9039c91da1" width="700">

#### 4.2 Testing the API with swagger UI

    http://localhost:8000/swagger/

## 5. Unit Testing

The API develop using the Test Driven Development TDD principle and modules have been tested with <a href="https://docs.python.org/3/library/unittest.html" target="_blank">unittest</a> by means of factory data from the factory boy library.

#### 5.1. Running Testcases

The test runner used in this project is <a href="https://docs.pytest.org/en/stable/contents.html" target="_blank">pytest</a>. Use the following command to run the unit test:

     python manage.py videoflix_tests (for Windows users)
     python3 manage.py videoflix_tests (for MAC or Linux users)

#### 5.2. Coverage Report

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

## 6. Celery and Redis: Caching, Task Queuing and Scheduling

For requests optimization to the endpoint, <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> was used to cache request data every 15 minutes since the data are not intended to be changed very often.
<a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">Celery</a> and <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a>

## 7. Periodic Data Import Export

The Data can be exported either manually or let be exported by our tasks runner: <a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">celery worker</a>

#### 7.1 Exporting DB Data manually

The manual export can be achieve by running the following command in the terminal:

    python manage.py export_video_data (for Windows users)
    python3 manage.py export_video_data (for MAC or Linux users)

#### 7.2 Exporting DB Data periodically

To avoid a possible loss of data when the server is broken the database is periodically exported as json file. This export has been scheduled using django celery beat which send the task to celery worker that in turn uses its broker (here <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a>) for running the task in the background every Sunday at 6AM.
For this purpose the django celery beat service should also be started the same way we did with celery(please make sure <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> is also running and update the password of redis in settings.py). The command to start django celery beat service is as follow:

    celery -A videoflix beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

In production this need to be done by the daemon of your system, for instance systemd. However, the periodic tasks will be set up when celery worker starts and do not need to be done manually in the admin panel. Visit the admin panel to see the setting under Crontab.

## Author

Ibrahima Sourabie
contact@ibrahima-sourabie.com
