
import streamlit as st
from multiapp import MultiApp
import staging_recipe_review
import inged_list_st  # import your app modules here
import categorisation
import mealTime
import add_ingredient

app = MultiApp()

# Add all your application here
app.add_app("Recipe Entry", inged_list_st.app)
app.add_app("Recipe Review and Release", staging_recipe_review.app)
app.add_app("Categorisation", categorisation.app)
app.add_app("Meal Time", mealTime.app)
app.add_app("Add/Edit Ingredients", add_ingredient.app)
# The main app
app.run()
