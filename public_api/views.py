from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Create your views here.

class get_data_endpoint_public(APIView):
    
    def get(self, request):
        
        data = requests.get('https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT',)

        return Response(data.json())
