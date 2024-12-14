from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.core.cache import cache

# Create your views here.

BINANCE_API = "https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT"
COINGECKO_API = "https://api.coingecko.com/api/v3/coins/bitcoin"


class get_price(APIView):
    
    def get(self, request):
        
        data = requests.get(BINANCE_API)
        response = data.json()

        context = {'price': response['price']}

        return Response(context)



class get_about(APIView):
    
    def get(self, request):

        data = requests.get(COINGECKO_API)

        data_cached = cache.get('DADOS_JSON')

        if data_cached: 
            return Response(data_cached)
        
        response = data.json()
        
        context = {
            "title": response['name'],
            "body": response['description']['en'],
        }

        cache.set('DADOS_JSON', context, timeout=600)
        return Response(context)
