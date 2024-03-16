import streamlit as st
import pandas as pd
import numpy as np
# st.title("Hi from my room new")
# st.markdown('### My streamlit dashboead')


DATA_URL = (
    "./Motor_Vehicle_Collisions_-_Crashes.csv"
)


st.title("Motor vehicle Collisions in New York City")

st.markdown("This application is a Steamlit dashboard that can be used to analyse motor vehicle collisions in NYC 🗽💥🚗")

# rerun the function only if the code or input changed
@st.cache_data(persist=True)
def load_data(nrows) :
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])

    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)

    lowercase= lambda x: str(x).lower()

    data.rename(lowercase, axis='columns', inplace=True)

    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


data = load_data(100000)









if st.checkbox("Show Raw Deta",False):
    st.subheader('Raw Data')
    st.write(data)