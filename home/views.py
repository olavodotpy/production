from django.shortcuts import render
import requests

PRODUCTION_URL = "https://production-production-8490.up.railway.app"
LOCALHOST = "http://127.0.0.1:8000"
ROOT_HTML = "home.html"
ABOUT_HTML = "about.html"

# Create your views here.


def home_view(request):
    data = requests.get(PRODUCTION_URL + "/api/consult/price")

    return render(request, ROOT_HTML, data.json())


def about_view(request):
    data = requests.get(PRODUCTION_URL + "/api/consult/about")

    return render(request, ABOUT_HTML, data.json())
