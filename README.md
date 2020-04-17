# APIcrm
This is an API REST API to manage customer data for a small shop. It will  work  as  the  backend  side  for  a  CRM  interface.

# Technologies
* Python
* Flask
* Docker
* PostgreSQL
* GCP Storage

# Local Development
To storage images, this project use a GCP bucket, so it's important create or use a GCP project and create a bucket.

When bucket it's ready, you should create a `.env` file into root diretory with this environment variables:
* **APP_SETTINGS**=config.Development (config options are listed into `config.py`)
* **DATABASE_URL**=postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_CONTAINER}:5432/{POSTGRES_DB}
* **SECRET_KEY**=Key to encode and decode jwt
* **GOOGLE_APPLICATION_CREDENTIALS**=Service account credentials from GCP project with storage permissions (just download service accounts json file and place it into root directory)
* **BUCKET_NAME**=Storage bucket name
* **POSTGRES_USER**=user to log into database
* **POSTGRES_PASSWORD**=user password to log into database
* **POSTGRES_DB**=postgres database name

To start working you can execute:
* `make docker_up` or `docker-compose up`
* `make docker_up_background` or `docker-compose up -d` to run containers in background

The options above build and run two containers:
* Database as *crmdb*
* API as *apicrm*

Once containers are up, the first time we start working on this project we should execute `make init_db_tables` 
command which initialize database tables.
Every time we need to update database tables, we should run command `make update_db_tables`.

Since you need an user to start making requests, you should execute the nexts commands:
* `docker exec -it DB-CONTAINER bash` (in order to enter into db container)
* `psql -U POSTGRES_USER -W -d POSTGRES_DB` (connet to database, after this command you will prompt to enter POSTGRES_PASSWORD)
* `insert into users (id, name, email, password, role) values (1, 'admin', 'admin@admin.es', '\x243262243132243332445434796c4f45517a68465763663572616771654a315434662e637549764e573659526c766a7a53664a53466e582e65544f4f', 1);`

It will create an admin user with:
* **email**: admin@admin.es
* **password**: adminapicrm

# Project Structure
### controllers
Into this folder you should put all database logic.
### models
Database models with some parser functions.
### utils
Divided in som folders:
* **auth**: Functions to use when validate auth information.
* **bucket**: Function to storage photos into GCP Bucket.
* **errors**: Error handlers
* **validators**: As his own name indicates, functions to validate data.
### app.py
Main file where database connection is stablished, and endpoints are declared.
### config.py
Some configuration options for different environments.
### docker-compose & Dockerfile
Since this project works with containers, we hace a Dockerfile to build API image, and a docker-compose file to create api and database containers.
### Makefile
File with commands to facilitate some operations.
### manage.py
File where set configuration to runserver and migrate/upgrade database models.
### requirements
Project's requirements.