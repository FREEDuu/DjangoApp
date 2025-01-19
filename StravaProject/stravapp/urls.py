from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path("", views.register, name="register"),
    path('login_strava/', views.login_strava, name='login_strava'),
    path('strava_redirect', views.strava_redirect, name='strava_redirect'),
    path('download_activity/', views.download_activity, name='download_activity'),
    path('csv_runs/', views.csv_runs, name='csv_runs'),
    path('UTMB_scrape/', views.UTMB_scrape, name='UTMB_scrape'),
    path('data_race/<str:race_id>', views.data_race, name='data_race')
    
]