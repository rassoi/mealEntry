import streamlit as st
import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from PIL import Image
import ast
from upload_images import upload_recipe, upload_ingred
import streamlit as st
import streamlit_authenticator as stauth
from google.oauth2 import service_account
# st.set_page_config(layout="wide")
key_dict = json.loads(st.secrets["textkey1"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="rassoi-767af")


def app():

    names = ['rassoi']
    usernames = ['rassoi']
    passwords = ["1234"]
    hashed_passwords = stauth.hasher(passwords).generate()
    authenticator = stauth.authenticate(names, usernames, hashed_passwords,
                                        'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

    name, authentication_status = authenticator.login('Login', 'main')
    key_dict = json.loads(st.secrets["textkey1"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="rassoi-767af")

    userList = db.collection(u'users').stream()
    uid_list = []
    for user in userList:
        uid = db.collection(u'users').document(user.id).get().to_dict()["uid"]
        uid_list.append(uid)

    user_tupple = tuple(i for i in uid_list)

    uid = st.selectbox("uid", (user_tupple))

    if (len(uid) > 5):

        ingred_list = db.collection(u'meal_ingred').where(
            u'user_uid', u'==', uid).stream()
        for ingred in ingred_list:
            ingredient = db.collection(u'meal_ingred').document(ingred.id).get().to_dict()
            if ingredient["meal_count"]>0:
                

                print(ingredient[""])
            
