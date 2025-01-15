from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Runner(models.Model):

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    expire_date_token = models.DateTimeField()

class Activity(models.Model):

    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    distance = models.FloatField()
    moving_time = models.BigIntegerField()
    elapsed_time = models.BigIntegerField()
    total_elevation_gain = models.FloatField()
    type = models.CharField(max_length=200)
    sport_type = models.CharField(max_length=200)
    kudos_count = models.IntegerField()
    average_speed = models.FloatField()
    max_speed = models.FloatField()
    start_date = models.DateTimeField(default=datetime.now())
