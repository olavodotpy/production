from django.shortcuts import render
import requests

PRODUCTION_URL = "https://production-production-8490.up.railway.app/api-private/consult/price"
LOCAL_URL = "http://127.0.0.1:8000/api-private/consult/price"
ROOT_HTML = "home.html"

# Create your views here.

def home_view(request):
    data = requests.get(PRODUCTION_URL)
    response = data.json()

    context = {'message': 'Hello, World', 'price': response['data']['price']}

    return render(request, ROOT_HTML, context)
