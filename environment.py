import os

## Values for development purpose

class ENV:
    APP_SETTINGS = 'config.DevelopmentConfig'
    DATABASE_URL = 'postgresql://postgres:postgres@apidb:5432/crm'
    SECRET_KEY = '\xf2D\xb2\xd8\xc0=\t\xcd\xcdd\x95\x00\x80\xa7]\x92\x975w\x1aW\xad\xdf\xa0'
    GOOGLE_APPLICATION_CREDENTIALS = 'apicrm-274115-0a9808857b88.json'
    BUCKET_NAME = 'api-crm-storage'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'postgres'
    POSTGRES_DB = 'crm'