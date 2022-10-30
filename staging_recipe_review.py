import streamlit as st
from firebase_admin import firestore
from google.oauth2 import service_account
import json


def app():
    key_dict = json.loads(st.secrets["textkey1"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="rassoi-767af")

    def get_temp_recipe_list():
        recipes_temp = db.collection(u'recipes_temp').stream()
        recipe_list = []
        recipe_list.append(".")
        for doc in recipes_temp:
            a = f'{doc.id}'
            # print("recipe ", a)
            recipe_list.append(a.lower())
        return recipe_list

    def get_ingred():
        ingred_list = []
        ingred = db.collection(u'ingredients').stream()
        for doc in ingred:
            a = f'{doc.id}'
            ingred_list.append(a.lower())
        return ingred_list

    def get_categories():
        categories_list = []
        categories_collection = db.collection(u'categories').stream()
        for doc in categories_collection:
            recipe_details = db.collection(
                u'categories').document(doc.id).get().to_dict()

            categories_list.append(f'{recipe_details["categoryName"]}')
        return categories_list

    def get_sub_categories():
        categories_list = []
        response = db.collection(u'miscellaneous').document(
            u'subCategories').get().to_dict()
        return response['name']

    recipe_list = get_temp_recipe_list()

    # st.write(recipe_list)
    recipe_tupple = tuple(i for i in recipe_list)

    recipe_id_dropdown = st.selectbox(
        "Type Meal ID", (recipe_tupple))

    if recipe_id_dropdown != ".":
        recipe_details = db.collection(u'recipes_temp').document(
            recipe_id_dropdown).get().to_dict()

        # st.write("Meal Id :", recipe_id_dropdown)
        # st.write("name : ", recipe_details["name"])
        # st.write("name_hindi : ", recipe_details["name_hindi"])
        # st.write("categoryName : ", recipe_details["categoryName"])
        # st.write("image : ", recipe_details["image"])
        # st.write("recipe_id : ", recipe_details["recipe_id"])
        # st.write("youtube_link : ", recipe_details["youtube_link"])
        # st.write("status : ", recipe_details["status"])
        # st.write("ref :", recipe_details["ref"])
        categories = ["All"]+get_categories()
        subCategories = ["None"]+get_sub_categories()
        name = st.text_input('name', recipe_details["name"])
        name_hindi = st.text_input('name_hindi', recipe_details["name_hindi"])
        print("multi select", recipe_details["categoryName"])
        print("categories", categories)
        categoryName = st.multiselect(
            'categoryName', categories, recipe_details["categoryName"])

        # if len(recipe_details["subCategories"]) == 1:
        #     subCategoryName = st.multiselect(
        #         'SubCategoryName',  subCategories, [])
        # else:
        subCategoryName = st.multiselect(
            "abc",  subCategories, recipe_details["subCategories"])
        if recipe_details["mealTime"]:
            exisiting_meal_type = recipe_details["mealTime"]
        else:
            exisiting_meal_type = []
        select_meal_time = st.multiselect(
            'mealaTime', ["Brakefast", "Lunch", "Snacks", "Dinner"], exisiting_meal_type)

        image = st.text_input('image', recipe_details["image"])
        st.write("recipe_id : ", recipe_details["recipe_id"])
        youtube_link = st.text_input(
            'youtube_link', recipe_details["youtube_link"])
        status = st.text_input('status', recipe_details["status"])
        st.write("ref :", recipe_details["ref"])
        veg = st.checkbox('Veg', recipe_details["veg"])

        st.write("Ingredients")

        ingred_list = db.collection(u'recipes_temp').document(
            recipe_id_dropdown).collection("ingreds").stream()
        # print(ingred_list)

        for ingredDoc in ingred_list:
            ingredId = ingredDoc.id
            print("ingred", ingredId)
            # st.write(ingredId)
            ingred_detail = db.collection(u'ingredients').document(
                ingredDoc.id).get().to_dict()
            print(ingred_detail)
            st.write(ingred_detail)
            remove = st.button("Remove "+ingredId)
            if remove:

                ingred_list = db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).collection("ingreds").document(ingredDoc.id).delete()
        select_ingred = st.multiselect('select ingred',
                                       get_ingred())

        if st.button("Verify changes"):
            if name != recipe_details["name"]:
                st.write("updated name to  ", name)
                db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).update({"name": name})
            if name_hindi != recipe_details["name_hindi"]:
                st.write("updating name_hindi to ", name_hindi)
                db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).update({"name_hindi": name_hindi})
            if categoryName != recipe_details["categoryName"]:
                st.write("updating categoryName to ", categoryName)
                db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).update({"categoryName": categoryName})
            if subCategoryName != recipe_details["subCategories"]:
                st.write("updating Sub categoryName to ", subCategoryName)
                db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).update({"subCategories": subCategoryName})
            if image != recipe_details["image"]:
                st.write("updating image to ", image)
                db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).update({"image": image})
            if youtube_link != recipe_details["youtube_link"]:
                st.write("updating youtube_link to ", youtube_link)
                db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).update({"youtube_link": youtube_link})
            if status != recipe_details["status"]:
                st.write("updating status to ", status)
                db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).update({"status": status})

            if select_meal_time != exisiting_meal_type:
                st.write("updating mealTime to ", select_meal_time)
                db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).update({"mealTime": select_meal_time})
            for item in select_ingred:
                ingred_detail = db.collection(
                    u'ingredients').document(item).get().to_dict()
                st.write("addding ", ingred_detail)
                ingred_detail = db.collection(
                    u'ingredients').document(item).get().to_dict()
                ingred_list = db.collection(u'recipes_temp').document(
                    recipe_id_dropdown).collection("ingreds").document(item).set(ingred_detail)

        if st.button("Submit as Recipe"):

            main_list = []

            name_split = name.split(" ")
            for word in name_split:
                print(word)
                j = ""
                for char in word.lower():
                    j = j+char
                    main_list.append(j)
            main_list.append(name)
            main_list.append(" ")
            main_list.append("")
            main_list_with_category = main_list
            for category in categoryName:

                main_list_with_category = main_list_with_category + \
                    [category+x for x in main_list]

            recipe_payload = {
                "name": name,
                "image": image,
                "name_hindi": name_hindi,
                "categoryName": categoryName,
                "nameAsArray": main_list_with_category,
                "recipe_id": recipe_details["recipe_id"],
                "youtube_link": youtube_link,
                "status": "live",
                "veg": veg,
                u"subCategories": subCategoryName
            }
            st.write(recipe_payload)

            db.collection(u'recipes').document(
                recipe_id_dropdown).set(recipe_payload)

            ingred_ref = db.collection(u'recipes_temp').document(
                recipe_id_dropdown).collection(u'ingreds').stream()
            ingreds = ""
            for ingred_doc in ingred_ref:
                ingred_ref = db.collection(u'ingredients').document(
                    ingred_doc.id).get().to_dict()
                # st.write(ingred_ref)
                ingreds = ingred_ref["english"]+"+"+ingred_doc.id+"+" + \
                    ingred_ref["hindi"]+"+"+ingred_ref["img"]+"*"+ingreds

            recipe_payload.update({"ref": db.collection(
                'recepies').document(recipe_id_dropdown)})

            recipe_payload.update({"ingred_names": ingreds})

            db.collection(u'recipes').document(
                recipe_id_dropdown).set(recipe_payload)

            ingred_list = db.collection(u'recipes_temp').document(
                recipe_id_dropdown).collection("ingreds").stream()

            for ingredDoc in ingred_list:
                ingredId = ingredDoc.id
                print("ingred", ingredId)
                st.write(ingredId)
                ingred_detail = db.collection(u'ingredients').document(
                    ingredId).get().to_dict()
                print(ingred_detail, type(ingred_detail))
                st.write(ingred_detail)
                # ingred_payload = {
                #     "english": ingred_detail["english"],
                #     "hindi": ingred_detail["hindi"],
                #     "img": ingred_detail["img"]
                # }
                db.collection(u'recipes').document(recipe_id_dropdown).collection(
                    "ingreds").document(ingredId).set(ingred_detail)
