import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse

from django.conf import settings

def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    headers = {'Content-Type': 'application/json'}
    
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret), headers=headers)
     
    response.raise_for_status() 
    result = response.json()
    access_token = result['access_token']
    if access_token:
        return JsonResponse({'access_token': access_token})
    else:
        return JsonResponse({"error:", response.status_code})
