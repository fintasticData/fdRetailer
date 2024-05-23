# -*- coding: utf-8 -*-
"""
Created on Wed May 22 16:39:43 2024

@author: dell
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt

st.image("fdLogo.png")
st.title("Logistics Dashboard")
st.write("Welcome to the Logistics  Dashboard. Here you can view key performance indicators and metrics that provide a comprehensive overview of the business performance.")


# Sample data for locations
data = {
    'Location': ['Warehouse', 'Store A', 'Store B', 'Store C'],
    'Latitude': [-1.2921, -1.2833, -1.2928, -1.3010],
    'Longitude': [36.8219, 36.8167, 36.8269, 36.8245]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate distances (Euclidean for simplicity)
def calculate_distance(lat1, lon1, lat2, lon2):
    return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

# Generate distance matrix
dist_matrix = np.zeros((len(df), len(df)))
for i in range(len(df)):
    for j in range(len(df)):
        dist_matrix[i][j] = calculate_distance(df.loc[i, 'Latitude'], df.loc[i, 'Longitude'], df.loc[j, 'Latitude'], df.loc[j, 'Longitude'])

# Streamlit App
st.title('Logistics Planning Dashboard')

# Step 1: Show locations on a map
st.subheader('Locations')
fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Location", zoom=14)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig)

# Step 2: Show distance matrix
st.subheader('Distance Matrix')
st.dataframe(pd.DataFrame(dist_matrix, columns=df['Location'], index=df['Location']))

# Step 3: Route Optimization
st.subheader('Route Optimization')
# Create a graph
G = nx.Graph()
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        G.add_edge(df.loc[i, 'Location'], df.loc[j, 'Location'], weight=dist_matrix[i][j])

# Get the shortest path using Dijkstra's algorithm
def shortest_path(graph, start, end):
    return nx.shortest_path(graph, source=start, target=end, weight='weight')

# Select start and end locations
start_location = st.selectbox('Select Start Location', df['Location'])
end_location = st.selectbox('Select End Location', df['Location'])

if st.button('Calculate Shortest Route'):
    path = shortest_path(G, start_location, end_location)
    st.write('Shortest Path:', ' -> '.join(path))
    st.write('Total Distance:', nx.shortest_path_length(G, source=start_location, target=end_location, weight='weight'))

    # Draw the path on the map
    path_df = df[df['Location'].isin(path)]
    path_fig = px.line_mapbox(path_df, lat="Latitude", lon="Longitude", hover_name="Location", zoom=14)
    path_fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(path_fig)

# Step 4: Route Optimization using TSP (Travelling Salesman Problem)
st.subheader('Travelling Salesman Problem (TSP) Optimization')
if st.button('Optimize Route for TSP'):
    tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)
    st.write('Optimized Route:', ' -> '.join(tsp_path))
    st.write('Total Distance:', nx.approximation.traveling_salesman_problem(G, cycle=True, weight='weight'))
    
    # Draw the TSP path on the map
    tsp_path_df = df[df['Location'].isin(tsp_path)]
    tsp_path_fig = px.line_mapbox(tsp_path_df, lat="Latitude", lon="Longitude", hover_name="Location", zoom=14)
    tsp_path_fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(tsp_path_fig)

st.write("With these insights, you can plan and optimize your logistics routes effectively.")
