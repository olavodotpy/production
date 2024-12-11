from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Create your views here.

class get_data_endpoint_public(APIView):
    
    def get(self, request):
        
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        data = requests.get(url)
        response = data.json()
        print(response)

        return Response(response)
