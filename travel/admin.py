from django.contrib import admin
from .models import Trip, Facility, EmergencyContact, Recommendation

admin.site.register(Trip)
admin.site.register(Facility)
admin.site.register(EmergencyContact)
admin.site.register(Recommendation)