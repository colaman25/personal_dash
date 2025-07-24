import streamlit as st
import pandas as pd
import numpy as np
import time
from st_files_connection import FilesConnection

conn2 = st.connection('s3', type=FilesConnection)
df2 = conn2.read("hylau-personal-dashboard-data/Calories_Daily.csv", input_format="csv", ttl=600)
df2.set_index('Date', inplace=True)
df2.sort_index(ascending=True, inplace=True)

df2['Calories_Avg_Month'] = df2['Calories_Intake'].rolling(window=30).mean()
df2['Calories_Avg_Year'] = df2['Calories_Intake'].rolling(window=365).mean()
df2['Calories_Avg_CMA'] = df2['Calories_Intake'].expanding().mean()
overall_mean = df2['Calories_Intake'].mean()

df2['Cans_Avg_Month'] = df2[df2.index >= '2025-06-10 00:00:00']['Cans'].rolling(window=30).mean()
df2['Cans_Avg_Year'] = df2[df2.index >= '2025-06-10 00:00:00']['Cans'].rolling(window=365).mean()
df2['Cans_Avg_CMA'] = df2[df2.index >= '2025-06-10 00:00:00']['Cans'].expanding().mean()
cans_overall_mean = df2[df2.index >= '2025-06-10 00:00:00']['Cans'].mean()

st.write(f'AVERAGE: {overall_mean:.0f}')
st.line_chart(df2[['Calories_Avg_Month', 'Calories_Avg_Year', 'Calories_Avg_CMA']].tail(365*5))

st.write(f'AVERAGE: {cans_overall_mean:.3f}')
st.line_chart(df2[df2.index >= '2025-06-10 00:00:00'][['Cans_Avg_Month', 'Cans_Avg_Year', 'Cans_Avg_CMA']].tail(365*5))