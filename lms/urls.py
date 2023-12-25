from django.urls import path
from .views import *
urlpatterns = [
path('', home, name='home'),
path('courses/', courses, name='courses'),
path('course/<str:slug>/', course_details, name='course_details'),
path('profile/', profile, name= 'profile'),
path('custom_logout/', custom_logout, name='custom_logout'),



#for checkout page 
path('dashboard/', dashboard, name='dashboard'),
path('course/<slug:slug>/enroll/', enroll, name='enroll'),
path('courses/<slug:course_slug>/playlist/', course_playlist, name='course_playlist'),



]