from celery import Celery
import requests
import os
import random
from celery import shared_task
from redis import Redis
from rest_framework import response

app = Celery('tasks', broker='redis://localhost:6379/0')
API_KEY =os.environ.get('API_KEY')
redis_connection = Redis(host='localhost', port=6002, db=0, charset='utf-8', decode_responses=True)
random_otp = str(random.randint(100000, 999999))




@shared_task()
def send_sms(phone_number):

    url = 'https://api.sms.ir/v1/send/verify/'            
    data = {                
        "mobile": phone_number, 
        "templateId": 100000,                
        "parameters": [  
            {                
                "name": "Code",                
                "value": random_otp             
            }            
        ]       
    }
    hedears = { 
        "Content-type": "application/json",
        "Accept": "text/plain",
        "x-api-key": API_KEY
    }     
       
    requests.post(url, json=data,headers=hedears)
          
    # print(response.json())
