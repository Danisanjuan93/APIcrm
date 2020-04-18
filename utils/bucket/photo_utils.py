import os
import base64
from datetime import datetime

from google.cloud import storage


def upload_customer_photo(customer, bs64_photo):
    storage_client = storage.Client()
    path_to_storage = "photos/{}-{}-{}".format(customer.id, customer.name, customer.surname)

    bucket = storage_client.get_bucket(os.environ['BUCKET_NAME'])
    blobs = bucket.list_blobs(prefix="{}/".format(path_to_storage))
    for blob in blobs:
        blob.delete()

    photo_extension = bs64_photo.split('/')[1].split(';')[0]
    content_type = 'image/' + photo_extension

    photo_name = "{}/{}-{}-{}-{}".format(path_to_storage, customer.id, customer.name, customer.surname, str(datetime.utcnow()))
    photo_data = bs64_photo.split(',')[1]

    bucket.blob(photo_name).upload_from_string(base64.b64decode(photo_data), content_type=content_type)

    bucket.blob(photo_name).make_public()
    return bucket.blob(photo_name).public_url

def remove_customer_photo(customer):
    storage_client = storage.Client()
    path_to_storage = "photos"

    bucket = storage_client.get_bucket(os.environ['BUCKET_NAME'])
    blobs = bucket.list_blobs(prefix="{}/".format(path_to_storage))
    for blob in blobs:
        if blob.name.split('/')[1] == f"{customer.id}-{customer.name}-{customer.surname}":
            blob.delete()
            break
