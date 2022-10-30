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


def app():

    key_dict = json.loads(st.secrets["textkey1"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="rassoi-767af")

    # print("Ingred list", ingred_list)

    def get_ingred():
        ingred_list = []
        ingred = db.collection(u'ingredients').stream()
        for doc in ingred:
            a = f'{doc.id}'
            ingred_list.append(a.lower())
        return ingred_list

    action = st.radio(
        "Select the action",
        ('Add', 'Edit'))

    if action == 'Add':

        ingred_list = ['.']
        ingred_list = ingred_list+get_ingred()
        ingred_id = st.text_input('enter ingred id')
        ingred_id = ingred_id.lower()
        if ingred_id in ingred_list:
            st.write("give another id")

        else:
            if len(ingred_id) > 2:
                st.write("name is ok")

        english_name = st.text_input(
            'english name', '')
        hindi_name = st.text_input(
            'Hindi name', '')
        image_url = st.text_input(
            'Image_url', '')

        img_name = "img_to_upload/"+ingred_id+".jpg"
        if len(image_url) > 10:
            response = requests.get(image_url)
            file = open(img_name, "wb")
            file.write(response.content)
            file.close()
            image = Image.open(img_name)
            st.image(
                image, caption=img_name, width=100)
            ingred_url = upload_ingred(ingred_id)
            upload_ingred_detail = {
                u'english': english_name,
                u'hindi': hindi_name,
                u'img': ingred_url

            }
            submit_ingred = st.button(
                "Submit Ingredient")
            ingred_ref = "/ingredients/"+ingred_id
            upload_ingred_ref = {
                u'reference': ingred_ref

            }

            if submit_ingred:

                db.collection(u'ingredients').document(
                    ingred_id).set(upload_ingred_detail)
    if action == "Edit":
        ingred_list = ["."] + get_ingred()
        ingred_tupple = tuple(i for i in ingred_list)
        ingred_id = st.selectbox(
            "Type Ingred ID", (ingred_tupple))
        if ingred_id != ".":
            response = db.collection(u'ingredients').document(
                ingred_id).get().to_dict()

            url = response.get('img')
            eng_name = response.get('english')
            hin_name = response.get('hindi')
            print("url", url)
            print("url", eng_name)
            print("url", hin_name)
            img_name = "images/"+ingred_id+".jpg"
            response = requests.get(url)
            file = open(img_name, "wb")
            file.write(response.content)
            file.close()

            image = Image.open(img_name)
            # st.write("English: ", eng_name)
            st.write("Hindi: ", hin_name)
            english = st.text_input('English name', eng_name)
            hindi = st.text_input('Hindi name', hin_name)

            st.image(image, caption=img_name, width=100)
            image_url = st.text_input('Change Image', url)

            img_name = "img_to_upload/"+ingred_id+".jpg"

            response = requests.get(image_url)
            file = open(img_name, "wb")
            file.write(response.content)
            file.close()
            image = Image.open(img_name)
            st.image(image, caption=img_name, width=100)

            submit_ingred = st.button(
                "Submit Ingredient")

            if submit_ingred:
                # db.collection(u'recipes_temp').document(meal_id).collection(
                #     u"ingreds").document(ingred_id).set(upload_ingred_ref)
                # db.collection(u'ingredients').document(
                #     ingred_id).set(upload_ingred_detail)
                # st.session_state.ingred_flags[i] = 1
                # upload_ingred_detail = {

                #     u'english': english,
                #     u'hindi': hindi,
                #     u'img': image_url

                # }
                if image_url != url:
                    print()
                    ingred_url = upload_ingred(ingred_id)
                else:
                    ingred_url = image_url

                if image_url != url or english != eng_name or hindi != hin_name:
                    # ingred_url = upload_ingred(ingred_id)
                    upload_ingred_detail = {

                        u'english': english,
                        u'hindi': hindi,
                        u'img': ingred_url

                    }
                    st.write("updating ", upload_ingred_detail)
                    db.collection(u'ingredients').document(
                        ingred_id).set(upload_ingred_detail)

                    recipe_temp = db.collection(u'recipes_temp').stream()
                    for recipe_temp_doc in recipe_temp:

                        ingre_temp = db.collection(u'recipes_temp').document(
                            recipe_temp_doc.id).collection(u"ingreds").stream()
                        for ingre_temp_doc in ingre_temp:
                            if ingre_temp_doc.id == ingred_id:
                                ingre_temp = db.collection(u'recipes_temp').document(recipe_temp_doc.id).collection(
                                    u"ingreds").document(ingre_temp_doc.id).set(upload_ingred_detail)

                else:
                    st.write("no changes")
