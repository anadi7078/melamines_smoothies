
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("Order need to be filled!")

cnx = st.connection("snowflake")
session = cnx.session()

# Only select orders where ORDER_FILLED = FALSE
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == False).collect()



if my_dataframe:
        editable_df = st.data_editor(my_dataframe)
        submitted = st.button('Submit')


        if submitted:
    # After submission, perform the merge operation
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)

    # Perform merge to update ORDER_FILLED based on the data edited in the Streamlit interface
    
            try:
                og_dataset.merge(
                    edited_dataset,
                    (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID']),
                    [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
            )
                st.success('Order(s) Updated!', icon='👍')
            except:
                st.write('Something went wrong')

else:
    st.success('Their is no order pending right now', icon='👍')
