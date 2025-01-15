import requests
from stravapp.models import Activity
from django.contrib.auth.models import User
from datetime import datetime

BASE_URL = "https://www.strava.com/api/v3/"

class STRAVA_API():
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def autorization(self, code):

        response = requests.post(
            url = f'https://www.strava.com/oauth/token?client_id={self.client_id}&client_secret={self.client_secret}&code={code}&grant_type=authorization_code'
        )
        return response.json()
    
    def retrieve_data(self, id, access_token):

        data_dumps = []

        for page in range(1, 5):
            response = requests.get(
                url=f"{BASE_URL}athlete/activities?access_token={access_token}&per_page={200}&page={page}",
            )
            data_dumps.append(response.json())

        bulk_activity_list = list()
        user = User.objects.get(id = id)

        for chunk in data_dumps:
            for run in chunk:
                bulk_activity_list.append(Activity(
                    id = run['id'],
                    user = user,
                    name = run['name'],
                    distance = run['distance'],
                    moving_time = run['moving_time'],
                    elapsed_time = run['elapsed_time'],
                    total_elevation_gain = run['total_elevation_gain'],
                    type = run['type'],
                    sport_type = run['sport_type'],
                    kudos_count = run['kudos_count'],
                    average_speed = run['average_speed'],
                    max_speed = run['max_speed'],
                    start_date = datetime.fromisoformat(run['start_date'].replace("Z", "+00:00"))
                ))

        Activity.objects.bulk_create(bulk_activity_list)