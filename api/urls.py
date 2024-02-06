
from django.contrib import admin
from django.urls import include, path
from .views import *
urlpatterns = [
  path('email',SendEmailView.as_view()),
  path('sms',SentSMSView.as_view())
  
]