import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

# st.title("Hi from my room new")
# st.markdown('### My streamlit dashboead')


DATA_URL = (
    "./Motor_Vehicle_Collisions_-_Crashes.csv"
)


st.title("Motor vehicle Collisions in New York City")

st.markdown("This application is a Steamlit dashboard that can be used to analyse motor vehicle collisions in NYC 🗽💥🚗")

# rerun the function only if the code or input changed
@st.cache_data()
def load_data(nrows) :
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])

    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)

    lowercase= lambda x: str(x).lower()

    data.rename(lowercase, axis='columns', inplace=True)

    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


data = load_data(100000)
original_data= data


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

hour = st.slider("Hour to look at",0,23) 
# hour = st.sidebar.slider("Hour to loor at",range(0,23)) 

#subset the data so that the date/time column match  the hour selected
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour,(hour+1) % 24))

#coodiante for the initial view state of the map
midpoint = (np.average(data['latitude']), np.average(data["longitude"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom" : 11,
        "pitch" : 50,   
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data = data[['date/time', 'latitude','longitude']],
            get_position=["longitude", "latitude"],
            radius=100,
            extruded = True, #for the 3D view
            pickable = True,
            elevation_scale = 4,
            elevation_range =[0,1000],
        ),
    ]
))

st.subheader("Breadown by minute between %i:00 and %i:00" %(hour,(hour+1)%24))
#filter the data 
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]

hist = np.histogram(filtered['date/time'].dt.minute,bins=60, range=(0,60))[0]

chart_data = pd.DataFrame({'minute':range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute',y='crashes',hover_data=['minute','crashes'], height = 400)

st.write(fig)

#
st.header("Top 5 dangerous streets by affected type")
select = st.selectbox('Affected type of people', ['Pedestrians','cyclists','Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >=1")[["on_street_name","injured_pedestrians"]].sort_values(by=['injured_pedestrians'],ascending=False).dropna(how='any')[:5])

elif select == 'Cyclits':
    st.write(original_data.query("injured_cyclists >=1")[["on_street_name","injured_cyclists"]].sort_values(by=['injured_cyclists'],ascending=False).dropna(how='any')[:5])

else:
    st.write(original_data.query("injured_motorists >=1")[["on_street_name","injured_motorists"]].sort_values(by=['injured_motorists'],ascending=False).dropna(how='any')[:5])


if st.checkbox("Show Raw Deta",False):
    st.subheader('Raw Data')
    st.write(data)