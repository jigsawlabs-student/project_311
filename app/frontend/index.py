import streamlit as st
import requests
import numpy as np
import plotly.offline as py
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt 
API_URL = "http://127.0.0.1:5000/incidents"
API_URL_AGENCIES = "http://127.0.0.1:5000/agencies"
API_URL_COMPLAINTS = "http://127.0.0.1:5000/complaints"

def get_incidents():
    response = requests.get(API_URL)
    return response.json()

#conneting to backend api localhost:5000/incidents
def get_agencies():
    response = requests.get(API_URL_AGENCIES)
    return response.json()

def get_complaints():
    response = requests.get(API_URL_COMPLAINTS)
    return response.json()


st.header('Incidents')
st.write('Here are locations of NYC 311 Service Requests')

def incident_locations(incidents):
    return [location['location'] for location in incidents]

def get_lat_long(location):
    get_coordinates = [location.get(k) for k in ['latitude', 'longitude', 'human_address']]
    return get_coordinates[:2]

def get_lat_longs(locations):
    return [get_lat_long(location) for location in locations]


incidents = get_incidents()
coordinates = get_lat_longs(incidents)

#this is my map of incidents
df = pd.DataFrame(coordinates, columns=['latitude', 'longitude'])
st.map(df)



def get_borough_names(incident_details):
    return [borough['borough'] for borough in incident_details]

def get_agency_complaint_counts(incident_details):
    return []

def get_agency_names(incident_detailss):
    return [agency['agency_name'] for agency in incident_details]

def get_type_of_complaints(incident_details):
    return [complaint['complaint_type'] for complaint in incident_details]

agency_data = go.Bar({'x': get_agency_names(incidents),
                 'y': get_agency_complaint_counts(agency)}, name= 'Incidents by Agency')
agency_layout = go.Layout(title = 'Most Utilized Agencies')
fig = go.Figure(data = agency_data, layout = agency_layout) 
go.plot(fig)

 

# data = [go.Bar(x = get_agency_names.index, y = agency_name.values, name = 'Most Utilized Agency')]
# layout = go.Layout(title = 'Most Utilized Agency')
# fig = go.Figure(data = data, layout = layout)
# go.plot(fig)

# scatter = go.Scatter(x = venue_names(venues, True), 
#         y = venue_ratings(venues, True), 
#         hovertext = venue_names(venues, True), mode = 'markers')

# locations = venue_locations(venues)


# fig = go.Figure(scatter)
# st.plotly_chart(fig)
# st.map(pd.DataFrame(locations))