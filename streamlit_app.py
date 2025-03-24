import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write("Choose the fruit you want in your custom Smoothie!")

# User input for the name on the smoothie
name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on smoothie is", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multi-select ingredients from the available fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe.to_pandas()['FRUIT_NAME'].tolist(),
    max_selections=5  
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Join selected fruits into a string

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)


    # Set ORDER_FILLED to FALSE by default (you can change this if needed)
    order_filled = False

    # Prepare the insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
        VALUES ('{name_on_order}', '{ingredients_string}', {order_filled})
    """

    # Create a button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered!', icon="✅")

