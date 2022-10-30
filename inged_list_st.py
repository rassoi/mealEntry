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
st.set_page_config(layout="wide")
key_dict = json.loads(st.secrets["textkey1"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="rassoi-767af")


def app():

    # st.set_page_config(layout="wide")
    names = ['rassoi']
    usernames = ['rassoi']
    passwords = ["1234"]
    hashed_passwords = stauth.hasher(passwords).generate()
    authenticator = stauth.authenticate(names, usernames, hashed_passwords,
                                        'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

    name, authentication_status = authenticator.login('Login', 'main')

    # if not firebase_admin._apps:
    #     cred = credentials.Certificate(
    #         'rassoi-767af-firebase-adminsdk-q09j7-a66f37f511.json')
    #     default_app = firebase_admin.initialize_app(cred)
    # db = firestore.Client.from_service_account_json(
    #     'rassoi-767af-firebase-adminsdk-q09j7-a66f37f511.json')

    key_dict = json.loads(st.secrets["textkey1"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="rassoi-767af")

    # db = firestore.client()

    if "ingred_substract" not in st.session_state:
        st.session_state.ingred_substract = []

    ingred_flag = 0

    def get_ingred():
        ingred_list = []
        ingred = db.collection(u'ingredients').stream()
        for doc in ingred:
            a = f'{doc.id}'
            ingred_list.append(a.lower())
        return ingred_list

    def Diff(li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

    def get_recipes():
        recipe_list = []
        recipies = db.collection(u'recipes').stream()
        for doc in recipies:
            # print(f'{doc.id}')
            recipe_list.append(f'{doc.id}')
        return recipe_list

    def get_recipes_temp():
        recipe_list = []
        recipies = db.collection(u'recipes_temp').stream()
        for doc in recipies:
            # print(f'{doc.id}')
            doc_id = doc.id
            recipe_list.append(doc_id["categoryName"])

        return recipe_list

    def get_sub_categories():
        categories_list = []
        response = db.collection(u'miscellaneous').document(
            u'subCategories').get().to_dict()
        return response['name']

    def get_categories():
        categories_list = []

        categories_collection = db.collection(u'categories').stream()
        for doc in categories_collection:
            categories_list.append(f'{doc.id}')
        # print(response['name'])
        return categories_list

    if authentication_status:

        ingred_list = []
        meal_details = {}
        # "https://www.youtube.com/watch?v=XeuY8Gy7w1Y&list=PLTmgqh9gERPKIc9w12Z66oG4uMICK6OFI&index=2" #st.text_input('Enter Youtube Link here', '')
        yt_link = st.text_input('YT link: ', '')

        if "meal_submitted_flag" not in st.session_state:
            st.session_state.meal_submitted_flag = 0
        else:
            pass

        if len(yt_link) > 2:

            id = yt_link[yt_link.index('=')+1:]
            id_image = id[:11]
            url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id='
            mid = '&key='
            ytapikey = "AIzaSyBkjBVZlEgKT5flbSVgfy4u38fOxrwHbyE"
            complete_url = url+id+mid+ytapikey
            r = requests.get(url=complete_url)
            response = r.json()
            text = response['items'][0]['snippet']['description']
            lines = text.split('\n')
            thumbnail_url = "https://img.youtube.com/vi/"+id+"/0.jpg"

            print("thumbnail_url", thumbnail_url)
            img_name = "img_to_upload_recipe/"+"temp"+".jpg"
            response = requests.get(thumbnail_url)
            file = open(img_name, "wb")
            file.write(response.content)
            file.close()
            st.image(img_name, caption=img_name, width=200)
            meal_id = st.text_input('Meal ID', '')
            meal_id = meal_id.lower()
            recipes = get_recipes() + get_recipes_temp()
            if meal_id in recipes:
                st.write("give another name")

            else:
                if len(meal_id) > 2:
                    st.write("name is ok")
                    # st.session_state.meal_id_flag = 1
            thumbnail_url = "https://img.youtube.com/vi/"+id+"/0.jpg"
            print("thumbnail_url", thumbnail_url)
            img_name = "img_to_upload_recipe/"+meal_id+".jpg"
            response = requests.get(thumbnail_url)
            file = open(img_name, "wb")
            file.write(response.content)
            file.close()

            meal_name = st.text_input('Meal Name', '')

            # meal_description = st.text_input('Meal Description', '')
            meal_name_hindi = st.text_input('Meal Name (Hindi)', '')
            # veg = st.radio(
            #     "Is the a Vegiterian Dish",
            #     ('Yes', 'No'))
            veg = st.checkbox('Veg', True)

            select_categories = st.multiselect(
                'select the categories',
                get_categories())
            select_categories.append("All")
            try:
                select_subcategories = st.multiselect(
                    'select the sub-categories',
                    get_sub_categories())
            except Exception as e:
                pass

            select_meal_time = st.multiselect(
                'select the meal time',
                ["Brakefast", "Lunch", "Snacks", "Dinner"])

            name_list = []
            for i in range(1, len(meal_name)):

                name_list.append(meal_name[0:i])

            # if "submit_meal_name" not in st.session_state:
            #     st.session_state.submit_meal_name = st.button("Submit Meal Name")
            #     st.session_state.submit_meal_name = True
            #     print("------", st.session_state.submit_meal_name)
            # else:

            if st.button("Submit Meal Name") == True and len(meal_id) > 1 and len(meal_name) > 1 and len(meal_name_hindi) > 1 or st.session_state.meal_submitted_flag == 1:
                # Uplad meal data
                st.session_state.meal_submitted_flag = 1
                meal_url = upload_recipe(meal_id)
                upload_meal_data = {
                    u'name': meal_name,
                    # u'desc': meal_description,
                    u'name_hindi': meal_name_hindi,
                    u'youtube_link': yt_link,
                    u'image': meal_url,
                    u'categoryName': select_categories,
                    u'mealTime': select_meal_time,
                    u'recipe_id': meal_id,
                    u"status": "live",
                    u"ref": "to be updated",
                    u"veg": veg,
                    u"subCategories": select_subcategories

                }
                db.collection(u'recipes_temp').document(
                    meal_id).set(upload_meal_data)

                ingred_list = ['.', "None"]
                ingred_list = ingred_list+get_ingred()

                ingred_tupple = tuple(i for i in ingred_list)
                if "ingred_flags" not in st.session_state:
                    st.session_state.ingred_flags = [0] * len(lines)
                else:
                    pass

                for i, line in enumerate(lines):
                    if st.session_state.ingred_flags[i] == 0:

                        check = st.checkbox(str(i)+'.'+line)
                        if check:
                            ingred_dropdown = st.selectbox(
                                "Type the name of ingred"+str(i), (ingred_tupple))
                            if ingred_dropdown != "None" and ingred_dropdown != ".":
                                response = db.collection(u'ingredients').document(
                                    ingred_dropdown).get().to_dict()
                                # response = f'{doc_ref}'
                                # response = ast.literal_eval(response)
                                url = response.get('img')
                                eng_name = response.get('english')
                                hin_name = response.get('hindi')
                                print("url", url)
                                print("url", eng_name)
                                print("url", hin_name)
                                img_name = "images/"+ingred_dropdown+".jpg"
                                response = requests.get(url)
                                file = open(img_name, "wb")
                                file.write(response.content)
                                file.close()

                                image = Image.open(img_name)
                                st.write("English: ", eng_name)
                                st.write("Hindi: ", hin_name)
                                st.image(image, caption=img_name, width=100)
                                submit_ingred = st.button(
                                    "Submit Ingredient"+str(i))
                                st.write(
                                    "___________________________________________________________________________________________________________________________________")

                                ingred_ref = "/ingredients/"+ingred_dropdown
                                upload_ingred_ref = {
                                    u'english': eng_name,
                                    u'hindi': hin_name,
                                    u'img': url,

                                }
                                if submit_ingred:
                                    db.collection(u'recipes_temp').document(meal_id).collection(
                                        u"ingreds").document(ingred_dropdown).set(upload_ingred_ref)

                                    st.session_state.ingred_flags[i] = 1
                            if ingred_dropdown == "None":
                                ingred_id = st.text_input(
                                    'enter ingred id'+str(i), '')
                                ingred_id = ingred_id.lower()
                                # print("Ingred list", ingred_list)
                                if ingred_id in ingred_list:
                                    st.write("give another id")

                                else:
                                    if len(ingred_id) > 2:
                                        st.write("name is ok")

                                english_name = st.text_input(
                                    'english name'+str(i), '')
                                hindi_name = st.text_input(
                                    'Hindi name'+str(i), '')
                                image_url = st.text_input(
                                    'Image_url'+str(i), '')

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
                                        "Submit Ingredient"+str(i))
                                    ingred_ref = "/ingredients/"+ingred_id
                                    upload_ingred_ref = {
                                        u'english': english_name,
                                        u'hindi': hindi_name,
                                        u'img': ingred_url

                                    }

                                    if submit_ingred:
                                        db.collection(u'recipes_temp').document(meal_id).collection(
                                            u"ingreds").document(ingred_id).set(upload_ingred_ref)
                                        db.collection(u'ingredients').document(
                                            ingred_id).set(upload_ingred_detail)
                                        st.session_state.ingred_flags[i] = 1
                    else:
                        st.write(str(i)+'.'+line)

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')


# def get_sub_categories():
#     categories_list = []
#     response = db.collection(u'miscellaneous').document(
#         u'subCategories').get().to_dict()
#     # categories_collection = db.collection(u'categories').stream()
#     # for doc in categories_collection:
#     #     categories_list.append(f'{doc.id}')
#     print(response)


# get_sub_categories()
