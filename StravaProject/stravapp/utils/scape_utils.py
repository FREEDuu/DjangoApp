import requests

def get_all_races(base_url):
    response = requests.get(base_url+'all_races')   
    return response.json()['data_races']

def get_race_data(race_id, url):
    response = requests.get(url+'data_race/'+race_id)   
    return response.json()
    