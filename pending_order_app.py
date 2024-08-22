# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("Orders That need to be filled.")

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.orders").filter(col('ORDER_FILLED')==0).collect()
# st.dataframe(data=my_dataframe, use_container_width=True)


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    
    submitted = st.button('Submit')
    if submitted:
       
        
        og_dataset = session.table("smoothies.public.orders")
        
        try:
            
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
            )
            st.success("Order(s) Completed", icon="👍")
        except Exception as exc:
            st.write("Something Went Wrong.", exc)
else:
    st.success("There are no Pending Orders right now", icon="👍")
