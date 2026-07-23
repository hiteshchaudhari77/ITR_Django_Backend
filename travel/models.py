from django.db import models


class Trip(models.Model):

    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    budget = models.IntegerField()
    days = models.IntegerField(default=1)
    members = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Facility(models.Model):

    city = models.CharField(max_length=100)
    hotel = models.CharField(max_length=100)
    restaurant = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    police = models.CharField(max_length=100)
    bus_stand = models.CharField(max_length=100)
    railway_station = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class EmergencyContact(models.Model):

    city = models.CharField(max_length=100)
    ambulance = models.CharField(max_length=20)
    police = models.CharField(max_length=20)
    fire = models.CharField(max_length=20)
    helpline = models.CharField(max_length=20)

    def __str__(self):
        return self.city


class Recommendation(models.Model):

    city = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    best_time = models.CharField(max_length=100)
    transport = models.CharField(max_length=100)
    tip = models.TextField()

    def __str__(self):
        return self.city