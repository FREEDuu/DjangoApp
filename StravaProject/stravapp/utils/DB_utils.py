from stravapp.models import Runner, Activity
from datetime import datetime
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder

def save_runner_DB(request, runner_data):

    expire_date_token = datetime.fromtimestamp(runner_data['expires_at'])
    athlete_info = runner_data['athlete']

    if runner_presence_DB(request.user.id):
        return athlete_info['id']

    user = User.objects.get(id = request.user.id)
    runner = Runner.objects.create(
        id = athlete_info['id'],
        user = user,
        username = athlete_info['username'],
        first_name =  athlete_info['firstname'],
        last_name =  athlete_info['lastname'],
        city =  athlete_info['city'],
        refresh_token = runner_data['refresh_token'],
        access_token = runner_data['access_token'],
        expire_date_token = expire_date_token
    )

    return runner.id

def runner_presence_DB(id):
    if Runner.objects.filter(user = id).exists():
        return True
    return False

