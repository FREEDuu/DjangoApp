from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
import os
from django.http import JsonResponse
from stravapp.models import Runner, Activity
from stravapp.stravi_api.strava_api import STRAVA_API
from stravapp.utils.session_utils import check_strava_access, first_auth, handle_csv, get_json_runs
from dotenv import load_dotenv
from stravapp.utils.scape_utils import get_all_races,get_race_data
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

load_dotenv()

CLIENT_SECRET = os.getenv('client_secret')
CLIENT_ID = os.getenv('client_id')
API = STRAVA_API(CLIENT_ID, CLIENT_SECRET)
LOGIN_URL = os.getenv('login_url')
API_UTMB_ENDPOINT = os.getenv('secret_api_UTMB')

@login_required
def home(request):

    charts_runs = []
    strava_access = check_strava_access(request, API)
    if strava_access:

        runner = Runner.objects.get(user = request.user.id)
        if first_auth(request.user.id):
            API.retrieve_data(request.user.id , runner.access_token)

        charts_runs = get_json_runs(request.user.id)
    charts_runs = [
        {
            "start_date": activity["start_date"].isoformat(),  # Convert to ISO 8601
            "distance": activity["distance"],
            "elevation" : activity["total_elevation_gain"]
        }
        for activity in charts_runs
    ]
    return render(request, "main_page.html", {
        'strava_access' : strava_access,
        'name' : request.user.username,
        'charts_runs' : charts_runs,
        'activities_count' : len(charts_runs)
    })

@login_required(login_url='login')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='login')
def login_strava(request):
    return render(request, 'login_strava.html')

@login_required(login_url='login')
def strava_redirect(request):
        return HttpResponseRedirect(LOGIN_URL)

@login_required(login_url='login')
def download_activity(request):
    return render(request, 'download.html')

@login_required(login_url='login')
def csv_runs(request):

    current_date = datetime.now().strftime("%Y%m%d")
    filename = f"data_{current_date}.csv"
    csv_content = handle_csv(request)
    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

def UTMB_scrape(request):

    races_list = get_all_races(API_UTMB_ENDPOINT)
    print(races_list)
    return render(request, 'UTMB_scrape.html',{
        'races_list' : races_list,
        'API_UTMB_ENDPOINT' : API_UTMB_ENDPOINT
    })

def data_race(request, race_id):

    race_data = get_race_data(race_id, API_UTMB_ENDPOINT)
    print(race_data)
    return JsonResponse(race_data)