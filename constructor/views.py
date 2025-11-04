from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
import json

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')