import sys
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from PIL import Image
import io
from google.cloud import storage
from uuid import uuid4
from google.oauth2 import service_account
import json
import streamlit as st

# key_path = "rassoi-767af-7e7713730f9d.json"


# credentials = service_account.Credentials.from_service_account_file(
#     key_path,
#     scopes=["https://www.googleapis.com/auth/cloud-platform"],
# )
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
client = storage.Client(credentials=creds)

# image_url = "https://5.imimg.com/data5/AP/RS/MY-10613027/cumin-seeds-500x500.jpg" #we pass the url as an argument

bucket = client.get_bucket('rassoi-767af.appspot.com')


def upload_recipe(meal_id):
    blob_path = "images/recipes/"+meal_id+".jpg"
    blob = bucket.blob(blob_path)
    file_name = "img_to_upload_recipe/"+meal_id+".jpg"
    blob.upload_from_filename(file_name)
    blob.make_public()
    url = blob.public_url
    print(url)
    return(url)


def upload_ingred(ingred_id):
    blob_path = "/images/ingredients/"+ingred_id+".jpg"
    blob = bucket.blob(blob_path)
    file_name = "img_to_upload/"+ingred_id+".jpg"
    blob.upload_from_filename(file_name)
    blob.make_public()
    url = blob.public_url
    url = url.replace("%20", " ")
    print(url)
    return(url)
# cred = credentials.Certificate('rassoi-767af-firebase-a
# dminsdk-q09j7-a66f37f511.json')
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'gs://rassoi-767af.appspot.com'
# })
# bucket = storage.bucket()

# blob = bucket.blob("/images/recipes/cumin.jpg")
# new_token = uuid4()
# metadata  = {"firebaseStorageDownloadTokens": new_token}
# blob.metadata = metadata
# blob.upload_from_filename(filename="img_to_upload/cumin.jpg", content_type='image/jpg')
# img= Image.open('img_to_upload/cumin.jpg')
# img_byte_arr = io.BytesIO()
# img = img_byte_arr.getvalue()
# print("Image",type(img))
# print(type(image_data))
# blob = bucket.blob('/images/recipes/cumin.jpg')
# blob.upload_from_string(
#         img,
#         content_type='image/jpg'
#     )
# print(blob.public_url)
# blob_names = [blob.name for blob in bucket.list_blobs()]
# print(blob_names)
# print(blob.name)
