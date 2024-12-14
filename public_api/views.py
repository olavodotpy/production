from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.core.cache import cache
import os
import dotenv

# Create your views here.

dotenv.load_dotenv()


class get_price(APIView):
    
    def get(self, request):
        
        data = requests.get(os.getenv("BINANCE_API"))
        response = data.json()

        context = {'price': response['price']}

        return Response(context)



class get_about(APIView):
    
    def get(self, request):

        data = requests.get(os.getenv("COINGECKO_API"))

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
