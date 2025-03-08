import streamlit as st
import pandas as pd
import numpy as np
import time
from st_files_connection import FilesConnection

with st.form("my_form"):
   st.write("Inside the form")
   my_date = st.date_input('Date', value="today")
   my_minutes = st.number_input('Minutes', min_value=0)
   st.form_submit_button('Submit')

st.write(my_date)
st.write(my_minutes)