
import streamlit as st
from firebase_admin import firestore
from google.oauth2 import service_account
import json


def app():
    key_dict = json.loads(st.secrets["textkey1"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="rassoi-767af")

    def get_categories():
        categories_list = []
        categories_collection = db.collection(u'categories').stream()
        for doc in categories_collection:
            recipe_details = db.collection(
                u'categories').document(doc.id).get().to_dict()

            categories_list.append(f'{recipe_details["categoryName"]}')
        # categories_list = ["gravy_sabji", "dry_sabji",
        #                    "rice", "side_dish", "dal", "bread", "brakefast"]

        return categories_list

    def get_recipes():
        recipe_list = []
        recipies = db.collection(u'recipes_temp').stream()
        for doc in recipies:
            # print(f'{doc.id}')
            recipe_list.append(f'{doc.id}')
        return recipe_list

    categories = get_categories()

    recipe_tupple = tuple(i for i in categories)
    print(recipe_tupple)

    action = st.radio(
        "Select the action",
        ('Add', 'Remove'))

    recipes = get_recipes()

    option = st.selectbox(
        'Select Categories',
        recipe_tupple)

    category_adddition_list = []
    for i, recipe in enumerate(recipes):
        # st.write(recipe)
        recipe_details = db.collection(
            u'recipes_temp').document(recipe).get().to_dict()
        if action == "Add":
            print(recipe, option, recipe_details)
            if option not in recipe_details["categoryName"]:
                details = recipe + ", " + \
                    recipe_details["name"] + \
                    str(recipe_details["categoryName"])
                check = st.checkbox(str(i)+'.'+details)

                if check:
                    category_adddition_list.append(recipe)
                else:
                    if recipe in category_adddition_list:
                        category_adddition_list.append(recipe)
        if action == "Remove":
            if option in recipe_details["categoryName"]:
                details = recipe + ", " + \
                    recipe_details["name"] + \
                    str(recipe_details["categoryName"])
                check = st.checkbox(str(i)+'.'+details)

                if check:
                    category_adddition_list.append(recipe)
                else:
                    if recipe in category_adddition_list:
                        category_adddition_list.append(recipe)

    if action == "Add":

        if st.button("Add Submit") and action == "Add":
            st.write(option, " category is added to ", category_adddition_list)
            for item in category_adddition_list:

                db.collection(u'recipes_temp').document(
                    item).update({u"categoryName": firestore.ArrayUnion([option])})

    if action == "Remove":

        if st.button("Remove Submit") and action == "Remove":
            st.write(option, " category is removed to ",
                     category_adddition_list)
            for item in category_adddition_list:

                db.collection(u'recipes_temp').document(
                    item).update({u"categoryName": firestore.ArrayRemove([option])})
