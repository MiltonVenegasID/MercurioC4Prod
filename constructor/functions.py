from multiprocessing import context
import os
import string
import uuid
from dotenv import load_dotenv
import requests
from django.http import JsonResponse
import random
from .models import *


load_dotenv()

def hub_register(nombre, cta):
    api = os.getenv('API_HUB')
    id_rec = os.getenv('API_ID_CHECK')
    recovered_id = requests.get(id_rec + str(cta))
    if not recovered_id.text or recovered_id.status_code != 200:
        data = {
            "success": False,
            "message": "No existe registro de este usuario en nuestro sistema.",
            "ref": "Error"
        }
        return data
    
    else:
        json_data = recovered_id.json()
        if isinstance(json_data, list) and json_data:
            json_data = json_data[0]

        cliente_Id = json_data.get('idCliente', '')
        general_search = requests.get(api).json()
        matching_items = [
            item for item in general_search
            if str(item.get('idCliente', '')) == str(cliente_Id)
        ]
        
        if not matching_items:
            data = {
                "success": False,
                "message": "No existe registro de este usuario en nuestro sistema.",
                "ref": "Error"
            }
            return data
            
        if nombre and not any(item.get('nomCont') == nombre or item.get('Razon') == nombre for item in matching_items):
            data = {
                "success": False,
                "message": "El nombre proporcionado no coincide con nuestros registros.",
                "ref": "Error"
            }
            return data
        
        for item in matching_items:
            if not item['mailCont']:
                continue
            token = uuid.uuid4()
            if item['mailCont'] in GestoresCreationRequest.objects.values_list('email', flat=True):
                three_digits = ''.join(random.choices(string.digits, k=3))
                new_email = item['mailCont'].replace('@', f'{three_digits}@')
                email=new_email,
                data = {
                    'NombreCompleto': item['nomCont'],
                    'Telefono': '',
                    'Cta': general_search['noCliente'],
                    'TipoUsuario': item['tipoCont'],
                    'ref': item['idCliente'],
                    'email': item['mailCont'],
                    'empresa': nombre
                },
                token=token
                

            else:
                data = {
                    'NombreCompleto': item['nomCont'],
                    'Telefono': '',
                    'Cta': general_search['noCliente'],
                    'TipoUsuario': item['tipoCont'],
                    'ref': item['idCliente'],
                    'email': item['mailCont'],
                    'empresa': nombre
                },
                token=token
                
            
            

            
        return data
