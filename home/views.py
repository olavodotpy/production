from django.shortcuts import render
import requests

PRODUCTION_URL = "https://production-production-8490.up.railway.app"
LOCAL_URL = "http://127.0.0.1:8000"
ROOT_HTML = "home.html"
ABOUT_HTML = "about.html"

# Create your views here.


def home_view(request):
    data = requests.get(LOCAL_URL + "/api/consult/price")
    response = data.json()

    context = {'message': 'Hello, World', 'price': response['price']}

    return render(request, ROOT_HTML, context)


def about_view(request):
    data = requests.get(LOCAL_URL + "/api/consult/about")
    response = data.json()

    context = {
        "title": response['name'],
        "body": response['description']['en'],
    }

    return render(request, ABOUT_HTML, context)
