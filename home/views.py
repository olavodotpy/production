from django.shortcuts import render
import requests
import os
import dotenv

# Create your views here.

dotenv.load_dotenv()


def home_view(request):
    data = requests.get(os.getenv("PRODUCTION_URL") + "/api/consult/price")

    return render(request, os.getenv("ROOT_HTML"), data.json())


def about_view(request):
    data = requests.get(os.getenv("PRODUCTION_URL") + "/api/consult/about")

    return render(request, os.getenv("ABOUT_HTML"), data.json())
