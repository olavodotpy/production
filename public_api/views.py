from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Create your views here.

class get_data_endpoint_public(APIView):
    
    def get(self, request):
        try:
            # Use um timeout adequado para evitar bloqueios
            response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=10)
            
            if response.status_code == 200:
                return Response({"status": "success", "data": response.json()})
            else:
                return Response({"status": "error", "message": f"Error: {response.status_code} - {response.text}"}, status=response.status_code)
        
        except requests.exceptions.RequestException as e:
            return Response({"status": "error", "message": str(e)}, status=500)
