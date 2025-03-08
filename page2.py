import streamlit as st
import pandas as pd
import numpy as np
import time
from st_files_connection import FilesConnection

conn = st.connection('s3', type=FilesConnection)
df = conn.read("hylau-personal-dashboard-data/Lapse_Data.csv", input_format="csv", ttl=600)
df.sort_index(ascending=False, inplace=True)

df['Minutes_Avg_Month'] = df['Minutes'].rolling(window=30).mean()
df['Minutes_Avg_CMA'] = df['Minutes'].expanding().mean()
overall_mean = df['Minutes'].mean()

st.line_chart(df, x="Date", y="Minutes_Avg_Month")
st.line_chart(df, x="Date", y="Minutes_Avg_CMA")
st.write(f'AVERAGE: {overall_mean}')