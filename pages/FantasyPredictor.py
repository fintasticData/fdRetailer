# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:05:06 2024

@author: dell
"""

import streamlit as st
import requests
import pandas as pd
import random

# Your Football Data API token
api_token = '9cee9b48cbe34f249c3dbbffbed1334b'

# Set page configuration
st.set_page_config(page_title="EPL Match Fixtures", page_icon="⚽", layout="wide")

# Add your logo at the top of the page
st.image("fdLogo.png")

# Hide the Streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Title of the page
st.title("EPL Match Fixtures")

# User inputs for season and matchday
st.sidebar.header("Select Season and Matchday")
season = st.sidebar.selectbox("Season", options=[2021, 2022, 2023])
matchday = st.sidebar.slider("Matchday", min_value=1, max_value=38, value=1)

# Fetch EPL fixtures
url = f'http://api.football-data.org/v2/competitions/PL/matches?season={season}&matchday={matchday}'
headers = {'X-Auth-Token': api_token}
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract relevant information from the response
    fixtures = data['matches']
    
    # Display the fixtures in a table
    st.write(f"### EPL Fixtures - Season {season}, Matchday {matchday}")
    fixture_data = []
    for fixture in fixtures:
        match_info = {
            "Home Team": fixture['homeTeam']['name'],
            "Away Team": fixture['awayTeam']['name'],
            "Date": fixture['utcDate'],
            "Status": fixture['status']
        }
        fixture_data.append(match_info)

    fixture_df = pd.DataFrame(fixture_data)
    st.dataframe(fixture_df)
else:
    st.write('Failed to fetch data')

# Footer with a call to action
st.write("---")
st.header("Learn More About EPL")
st.write("For more information about the English Premier League, visit the official website.")
st.button("Explore More", on_click=lambda: st.write("Visit [Premier League](https://www.premierleague.com) for more information."))

# Footer link
st.write("---")
st.write("[Explore More >](https://www.premierleague.com)")


# Set page configuration
# st.set_page_config(page_title="Fantasy EPL Team Prediction", page_icon="⚽", layout="wide")

st.image("fdLogo.png")  
# Hide the Streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Title of the page
st.title("Fantasy EPL Team Prediction")

# Fetch player data
url = 'https://api.football-data.org/v2/competitions/PL/teams'
headers = {'X-Auth-Token': api_token}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    teams_data = response.json()['teams']
    
    # Collect players data
    players_data = []
    for team in teams_data:
        team_id = team['id']
        team_response = requests.get(f'https://api.football-data.org/v2/teams/{team_id}', headers=headers)
        if team_response.status_code == 200:
            players = team_response.json()['squad']
            for player in players:
                players_data.append({
                    'name': player['name'],
                    'position': player['position'],
                    'team': team['name'],
                    'nationality': player['nationality'],
                    'dateOfBirth': player['dateOfBirth']
                })
else:
    st.write('Failed to fetch data')

# Create a dataframe
players_df = pd.DataFrame(players_data)

# For simplicity, randomly assign points to players
players_df['points'] = [random.randint(0, 100) for _ in range(len(players_df))]

# Filter players by position
goalkeepers = players_df[players_df['position'] == 'Goalkeeper'].nlargest(2, 'points')
defenders = players_df[players_df['position'] == 'Defender'].nlargest(5, 'points')
midfielders = players_df[players_df['position'] == 'Midfielder'].nlargest(5, 'points')
forwards = players_df[players_df['position'] == 'Attacker'].nlargest(3, 'points')

# Combine the team
fantasy_team = pd.concat([goalkeepers, defenders, midfielders, forwards])

# Display the fantasy team
st.write("### Recommended Fantasy Team")
st.dataframe(fantasy_team[['name', 'position', 'team', 'points']])