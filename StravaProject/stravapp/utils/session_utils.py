from stravapp.utils.DB_utils import save_runner_DB,runner_presence_DB
from stravapp.models import Activity
import csv
from io import StringIO
from django.core.serializers import serialize


def set_session_id(request, id):
    
    request.session['StravaID'] = id
    request.session.save()

def check_session_id(request):
    
    if not request.session.get('StravaID'):
        return True
    return False

def check_strava_access(request, api):

    if runner_presence_DB(request.user.id):
        return True

    elif request.GET.get('code'):
        runner_data = api.autorization(request.GET.get('code'))
        id = save_runner_DB(request, runner_data)
        return True
    
    return False
    
def first_auth(id):
    if Activity.objects.filter(user = id).exists():
        return False
    return True

def handle_csv(request):

    
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer, delimiter=';')

    # Get only the necessary fields to avoid fetching entire objects
    runs = Activity.objects.filter(user=request.user.id).values(
        'id', 'user', 'name', 'distance', 'moving_time', 'elapsed_time', 
        'total_elevation_gain', 'type', 'sport_type', 'kudos_count', 
        'average_speed', 'max_speed'
    )

    # Column headers for the CSV
    columns = ['id', 'user', 'name', 'distance', 'moving_time', 
            'elapsed_time', 'total_elevation_gain', 'type', 
            'sport_type', 'kudos_count', 'average_speed', 'max_speed']

    # Write header to CSV
    writer.writerow(columns)

    # Write data rows to CSV in a single loop
    writer.writerows(
        [run['id'], run['user'], run['name'], run['distance'], run['moving_time'], 
        run['elapsed_time'], run['total_elevation_gain'], run['type'], 
        run['sport_type'], run['kudos_count'], run['average_speed'], 
        run['max_speed']] 
        for run in runs
    )
    
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_content

def get_json_runs(id):

    chart_runs = Activity.objects.filter(user = id).order_by('start_date').values('start_date', 'distance', 'total_elevation_gain')

    return list(chart_runs)

def format_run(run):
    return  {run['id'],
            run['user'], 
            run['name'], 
            run['distance'], 
            run['moving_time'], 
            run['elapsed_time'], 
            run['total_elevation_gain'],
            run['type'], run['sport_type'],
            run['kudos_count'],
            run['average_speed'], 
            run['max_speed']
            }