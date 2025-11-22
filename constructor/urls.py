from django.urls import path
from . import views
from django.urls import re_path as url
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

urlpatterns = [
    path('api/data/', views.home_view, name='receive_data'),
    url(r'^.*$/app', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'get-token/$', views.get_csrf_token)
]