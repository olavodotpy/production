from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Create your views here.

BINANCE_API = "https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT"
COINGECKO_API = "https://api.coingecko.com/api/v3/coins/bitcoin"




class get_price(APIView):
    
    def get(self, request):
        
        data = requests.get(BINANCE_API)

        return Response(data.json())



class get_about(APIView):
    
    def get(self, request):

        data = requests.get(COINGECKO_API)

        return Response(data.json())
