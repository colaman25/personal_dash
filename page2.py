import streamlit as st
import pandas as pd
import numpy as np
import time
from st_files_connection import FilesConnection

conn1 = st.connection('s3', type=FilesConnection)
df1 = conn1.read("hylau-personal-dashboard-data/Lapse_Data.csv", input_format="csv", ttl=600)
df1.set_index('Date', inplace=True)
df1.sort_index(ascending=True, inplace=True)

df1['Minutes_Avg_Month'] = df1['Minutes'].rolling(window=30).mean()
df1['Minutes_Avg_Year'] = df1['Minutes'].rolling(window=365).mean()
df1['Minutes_Avg_CMA'] = df1['Minutes'].expanding().mean()
overall_mean = df1['Minutes'].mean()

df1['Lapse_Avg_Month'] = df1[df1.index >= '2024-05-27 00:00:00']['Lure Lapse'].rolling(window=30).mean()
df1['Lapse_Avg_Year'] = df1[df1.index >= '2024-05-27 00:00:00']['Lure Lapse'].rolling(window=365).mean()
df1['Lapse_Avg_CMA'] = df1[df1.index >= '2024-05-27 00:00:00']['Lure Lapse'].expanding().mean()
overall_lapse_mean = df1[df1.index >= '2024-05-27 00:00:00']['Lure Lapse'].mean()

st.write(f'AVERAGE: {overall_mean:.2f}')
st.line_chart(df1[['Minutes_Avg_Month', 'Minutes_Avg_Year', 'Minutes_Avg_CMA']].tail(365*5))

st.write(f'AVERAGE: {overall_lapse_mean:.3f}')
st.line_chart(df1[df1.index >= '2024-06-15 00:00:00'][['Lapse_Avg_Month', 'Lapse_Avg_Year', 'Lapse_Avg_CMA']].tail(365*5))
