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
@st.cache(persist=True)
def load_data(nrows) :
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])

    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)

    lowercase= lambda x: str(x).lower()

    data.rename(lowercase, axis='columns', inplace=True)

    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


data = load_data(100000)


#filtering data

st.header("Where are the most injured people in NYC ?")


injured_poeple = st.slider("Number of Injured People in vehicle collisions", min_value=0, max_value=19)

#plot the data into a map
#filtering with query
#column name >= variable , return the ln and lat columns
st.map(data.query("injured_persons >= @injured_poeple")[["latitude","longitude"]].dropna(how="any")) 

#update the view on the map

st.header("How many collision occur during a given time of the day")

# hour = st.selectbox("Hour to loor at",range(0,24), 1)  slider is better

hour = st.slider("Hour to loor at",range(0,23)) 
# hour = st.sidebar.slider("Hour to loor at",range(0,23)) 

#subset the data so that the date/time column match  the hour selected
data = data[data['date/time'].dt.hour == hour]








if st.checkbox("Show Raw Deta",False):
    st.subheader('Raw Data')
    st.write(data)