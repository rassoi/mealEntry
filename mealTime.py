
import streamlit as st
from firebase_admin import firestore
from google.oauth2 import service_account
import json


def app():
    key_dict = json.loads(st.secrets["textkey1"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="rassoi-767af")

    def getMealtime():

        return ["Brakefast", "Lunch", "Snacks", "Dinner"]

    def get_recipes():
        recipe_list = []
        recipies = db.collection(u'recipes').stream()
        for doc in recipies:
            # print(f'{doc.id}')
            recipe_list.append(f'{doc.id}')
        return recipe_list

    mealTime = getMealtime()

    mealTime_tupple = tuple(i for i in mealTime)

    action = st.radio(
        "Select the action",
        ('Add', 'Remove'))

    recipes = get_recipes()

    option = st.selectbox(
        'Select Mealtime',
        mealTime_tupple)

    category_adddition_list = []
    for i, recipe in enumerate(recipes):
        # st.write(recipe)
        recipe_details = db.collection(
            u'recipes').document(recipe).get().to_dict()
        if action == "Add":
            if option not in recipe_details["mealTime"]:
                details = recipe + ", " + \
                    recipe_details["name"] + \
                    str(recipe_details["mealTime"])
                check = st.checkbox(str(i)+'.'+details)

                if check:
                    category_adddition_list.append(recipe)
                else:
                    if recipe in category_adddition_list:
                        category_adddition_list.append(recipe)
        if action == "Remove":
            if option in recipe_details["mealTime"]:
                details = recipe + ", " + \
                    recipe_details["name"] + \
                    str(recipe_details["mealTime"])
                check = st.checkbox(str(i)+'.'+details)

                if check:
                    category_adddition_list.append(recipe)
                else:
                    if recipe in category_adddition_list:
                        category_adddition_list.append(recipe)

    if action == "Add":
        if st.button("Add Submit") and action == "Add":
            st.write(option, " category is added to ", category_adddition_list)

    if action == "Remove":
        if st.button("Remove Submit") and action == "Remove":
            st.write(option, " category is removed to ",
                     category_adddition_list)
