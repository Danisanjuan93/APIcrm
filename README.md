# APIcrm
This is an API REST API to manage customer data for a small shop. It will  work  as  the  backend  side  for  a  CRM  interface. \n


# Local Development
To storage images, this project use a GCP bucket, so it's important create or use a GCP project and create a bucket.

When bucket it's ready, you should create a `.env` file into root diretory with this environment variables:
* *APP_SETTINGS*=config.Development (config options are listed into `config.py`)
* *DATABASE_URL*=postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_CONTAINER}:5432/{POSTGRES_DB}
* *SECRET_KEY*=Key to encode and decode jwt
* *GOOGLE_APPLICATION_CREDENTIALS*=Service account credentials from GCP project with storage permissions (just download service accounts json file and place it into root directory)
* *BUCKET_NAME*=Storage bucket name
* *POSTGRES_USER*=user to log into database
* *POSTGRES_PASSWORD*=user password to log into database
* *POSTGRES_DB*=postgres database name

To start working you can execute:
* `make docker_up` or `docker-compose up`
* `make docker_up_background` or `docker-compose up -d` to run containers in background

The options above build and run two containers:
* Database as *crmdb*
* API as *apicrm*

Once containers are up, the first time we start working on this project we should execute `make init_db_tables` 
command which initialize database tables.
Every time we need to update database tables, we should run command `make update_db_tables`.