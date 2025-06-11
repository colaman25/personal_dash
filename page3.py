import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import date
from datetime import datetime
from st_files_connection import FilesConnection

def write_to_df_calories():

    date_index = str(datetime.combine(st.session_state.date, datetime.min.time()))
    st.session_state.df2.loc[date_index] = [st.session_state.calories, st.session_state.cans]
    st.session_state.df2.sort_index(ascending=False, inplace=True)

    st.dataframe(st.session_state.df2)

    conn2 = st.connection('s3', type=FilesConnection)
    with conn2.open("hylau-personal-dashboard-data/Calories_Daily.csv", mode='wb') as f:
        st.session_state.df2.to_csv(f)
    f.close()


if 'df2' not in st.session_state:
    conn2 = st.connection('s3', type=FilesConnection)
    st.session_state.df2 = conn2.read("hylau-personal-dashboard-data/Calories_Daily.csv", input_format="csv", ttl=600)
    st.session_state.df2.set_index('Date', inplace=True)

    st.dataframe(st.session_state.df2)

exist_value_calories = st.session_state.df2['Calories_Intake'].iloc[0]

with st.form("my_form"):
   st.write("Calories")
   st.date_input('Date', value='today', key='date')
   st.number_input('Calories', min_value=0, value=exist_value_calories, key='calories')
   st.number_input('Cans', min_value=0, key='cans')
   submit = st.form_submit_button('Submit', on_click=write_to_df_calories)
