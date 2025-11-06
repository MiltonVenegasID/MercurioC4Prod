from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
import json
from .forms import *

class HomeView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'home.html', {'form': form})