from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Trip
    path('trip/', views.trip, name='trip'),
    path('edit/<int:id>/', views.edit_trip, name='edit_trip'),
    path('delete/<int:id>/', views.delete_trip, name='delete_trip'),

    # Facility
    path('facility/', views.facility, name='facility'),

    # Emergency
    path('emergency/', views.emergency, name='emergency'),

    # Recommendation
    path('recommendation/', views.recommendation, name='recommendation'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]