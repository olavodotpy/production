from django.shortcuts import render
import requests

PRODUCTION_URL = "https://production-production-8490.up.railway.app/api/consult/price"
LOCAL_URL = "http://127.0.0.1:8000/api/consult/price"
ROOT_HTML = "home.html"

# Create your views here.

def home_view(request):
    data = requests.get(PRODUCTION_URL)
    response = data.json()

    context = {'message': 'Hello, World', 'price': response['price']}

    return render(request, ROOT_HTML, context)
