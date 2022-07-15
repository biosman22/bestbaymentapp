import requests, json
from datetime import datetime, timedelta 
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils import timezone
from django.conf import settings
from .signature import get_signature
from .api_call import call_api

def get_countries():
    http_method = 'get'                   # get|put|post|delete - must be lowercase
    path = '/v1/data/countries' 
    
    results = call_api(http_method, path=path)

   # print(results.json())
    return results.json()



def create_wallet():
    path = "/v1/user"
    http_method = "post"



    d  = json.dumps( {
    "first_name":"John",
    "last_name":"Doe",
    "email":"",
    "ewallet_reference_id":"John-Doe-03189020",
    "metadata":{
        "merchant_defined": True
    },
    "phone_number":"",
    "type":"person",
    "contact":{
        "phone_number":"+14155581234",
        "email":"johnfdoe1@rapyd.net",
        "first_name":"John",
        "last_name":"Doe",
        "contact_type":"personal",
        "address":{
            "name":"John Doe",
            "line_1":"123 Main Street",
            "line_2":"",
            "line_3":"",
            "city":"Anytown",
            "state":"NY",
            "country":"US",
            "zip":"12345",
            "phone_number":"+14155581234",
            "metadata":{},
            "canton":"",
            "district":""
        },
        "identification_type":"PA",
        "identification_number":"12345458890",
        "date_of_birth":"11/22/2000",
        "country":"US",
        "metadata":{
            "merchant_defined":True
        }
        }
    }, separators=(',', ':'))

    r= call_api(http_method, path, body=d)

    print(r.json())



def country_required_documents():

    country = 'US'

    results = call_api('get', path=f'/v1/identities/types?country={country}')

    print(results.json())


def verify_identity():
    wallet_id = 'ewallet_87f92e979eda240f859d33d25b58b4ee'

    idv_details = json.dumps({
        "reference_id": "555",
        "ewallet": wallet_id,
        "country": "US",
        "document_type": "PA",
        "front_side_image": "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",
        "front_side_image_mime_type": "image/jpeg",
        "face_image": "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",
        "face_image_mime_type": "image/jpeg",
        "request_type": "store"
    }, separators=(',', ':'))

    results = call_api('post', path=f'/v1/identities', body=idv_details)

    print(results.json())



def create_virtual_bank_account():
    
    body = json.dumps({
        "currency": "GBP",
        "country": "GB",
        "description": "Issuing bank account number to wallet",
        "ewallet": "ewallet_87f92e979eda240f859d33d25b58b4ee",
    }, separators=(',', ':'))

    results = call_api('post', path=f'/v1/issuing/bankaccounts', body=body)

    print(results.json())
    print("virtual account created ")



def list_virtual_accounts():

    wallet_id = f'ewallet_87f92e979eda240f859d33d25b58b4ee'
    results = call_api('get', path=f'/v1/issuing/bankaccounts/list?ewallet='+wallet_id)
    
    print("all virtual accouns")

    print(results.json())


def bank_deposit():
    body = json.dumps({
	"issued_bank_account": "issuing_5ab20620229c02a7335258d699701d0e",
	"amount": "100",
	"currency": "GBP"
    }, separators=(',', ':'))
   
    results = call_api('post', path=f'/v1/issuing/bankaccounts/bankaccounttransfertobankaccount', body=body)
    
    print("all virtual accouns")

    print(results.json())