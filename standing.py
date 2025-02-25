from klucze import *
import requests
import pandas as pd
from pandas import json_normalize

class Standing:
    def __init__(self, standing_id: int, standing_pId: int, standing_position: int):
        self.standing_team = None
        endpoint = f"{Base_URL}/teams"
        params = {
            "api_token": API_token,
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            team_data = []
            for team in data['data']:
                team_name = team['name']
                team_id = team['id']
                team_data.append((team_name,team_id))
            for t in team_data:
                if(standing_pId == t[1]):
                    self.standing_team = t[0]
        else:
            print(f"Błąd: {response.status_code}")
        
        self.standing_pId = standing_pId
        self.standing_id = standing_id
        self.standing_position = standing_position
        #print("Object created!")
    
    def show(self):
        if self.standing_team is None:
            return(f"{self.standing_id} - {self.standing_pId} - {self.standing_position}")
        else:
           return(f"{self.standing_id} - {self.standing_team} - {self.standing_position}") 
        