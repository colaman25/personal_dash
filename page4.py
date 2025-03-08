import streamlit as st
import pandas as pd
import numpy as np
import time
from st_files_connection import FilesConnection

conn = st.connection('s3', type=FilesConnection)
df = conn.read("hylau-personal-dashboard-data/Calories_Daily.csv", input_format="csv", ttl=600)
df.set_index('Date', inplace=True)
df.sort_index(ascending=True, inplace=True)

df['Calories_Avg_Month'] = df['Calories_Intake'].rolling(window=30).mean()
df['Calories_Avg_CMA'] = df['Calories_Intake'].expanding().mean()
overall_mean = df['Calories_Intake'].mean()

st.write(f'AVERAGE: {overall_mean:.0f}')
st.line_chart(df[['Calories_Avg_Month', 'Calories_Avg_CMA']])