import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import date
from datetime import datetime
from st_files_connection import FilesConnection

def write_to_df_lapse():

    date_index = str(datetime.combine(st.session_state.date, datetime.min.time()))
    st.session_state.df1.loc[date_index] = [st.session_state.minutes, st.session_state.lapse]
    st.session_state.df1.sort_index(ascending=False, inplace=True)

    st.dataframe(st.session_state.df1)

    conn1 = st.connection('s3', type=FilesConnection)
    with conn1.open("hylau-personal-dashboard-data/Lapse_Data.csv", mode='wb') as f:
        st.session_state.df1.to_csv(f)
    f.close()


# ----------------- Load Data -----------------
if 'df1' not in st.session_state:
    conn1 = st.connection('s3', type=FilesConnection)
    st.session_state.df1 = conn1.read("hylau-personal-dashboard-data/Lapse_Data.csv", input_format="csv", ttl=600)
    st.session_state.df1.set_index('Date', inplace=True)
    st.dataframe(st.session_state.df1)


# ----------------- Prepopulate Form -----------------
# Prepare today's date in index format
today_index = str(datetime.combine(date.today(), datetime.min.time()))

# Check if today's row exists
if today_index in st.session_state.df1.index:
    exist_value_minutes = int(st.session_state.df1.loc[today_index]['Minutes'])
    exist_value_lapse = int(st.session_state.df1.loc[today_index]['Lure Lapse'])
else:
    exist_value_minutes = 0
    exist_value_lapse = 0


# ----------------- Input Form -----------------
with st.form("my_form"):
   st.write("Daily Lapse")
   st.date_input('Date', value='today', key='date')
   st.number_input('Minutes', min_value=0, value = exist_value_minutes, key='minutes')
   st.selectbox('Lapse', (0, 1), index=exist_value_lapse, key='lapse')
   submit = st.form_submit_button('Submit', on_click=write_to_df_lapse)
