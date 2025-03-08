import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import date
from datetime import datetime
from st_files_connection import FilesConnection

def write_to_df():

    date_index = str(datetime.combine(st.session_state.date, datetime.min.time()))
    st.session_state.df.loc[date_index] = [st.session_state.minutes, st.session_state.lapse]
    st.session_state.df.sort_index(ascending=False, inplace=True)

    st.dataframe(st.session_state.df)

    conn = st.connection('s3', type=FilesConnection)
    with conn.open("hylau-personal-dashboard-data/Lapse_Data.csv", mode='wb') as f:
        st.session_state.df.to_csv(f)

if 'df' not in st.session_state:
    conn = st.connection('s3', type=FilesConnection)
    st.session_state.df = conn.read("hylau-personal-dashboard-data/Lapse_Data.csv", input_format="csv", ttl=600)
    st.session_state.df.set_index('Date', inplace=True)

    st.dataframe(st.session_state.df)


with st.form("my_form"):
   st.write("Daily Lapse")
   st.date_input('Date', value='today', key='date')
   st.number_input('Minutes', min_value=0, key='minutes')
   st.selectbox('Lapse', (0, 1), key='lapse')
   submit = st.form_submit_button('Submit', on_click=write_to_df)