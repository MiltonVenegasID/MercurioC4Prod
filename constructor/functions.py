from multiprocessing import context
import os
import string
import uuid
import requests
from django.http import JsonResponse
from django.core.mail import send_mail, get_connection
from django.conf import settings
import random
from .models import *

connection = get_connection(
    host=settings.SMTP_HOST,
    port=settings.SMTP_PORT,
    username=settings.SMTP_USERNAME,
    password=settings.SMTP_PASSWORD
)

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
            existing_count = GestoresCreationRequest.objects.filter(
                data__email=item['mailCont']
            ).count()
            
            if existing_count >= 3:
                continue
            
            if item['mailCont'] in GestoresCreationRequest.objects.values_list('email', flat=True):
                three_digits = ''.join(random.choices(string.digits, k=3))
                new_email = item['mailCont'].replace('@', f'{three_digits}@')
                GestoresCreationRequest.objects.create(
                    email=new_email,
                    data = {
                        'NombreCompleto': item['nomCont'],
                        'Telefono': '',
                        'Cta': cta,
                        'TipoUsuario': item['tipoCont'],
                        'ref': item['idCliente'],
                        'email': item['mailCont'],
                        'empresa': nombre
                    },
                    token=token
                )
                
                send_mail('Confirmación de registro - Acción requerida',
                        f'Estimado/a {item["nomCont"]},\n\nHemos notado que el correo electrónico proporcionado ya está en uso. '
                        f'Por favor, utilice el siguiente correo electrónico alternativo para completar su registro: {new_email}\n\nGracias por su comprensión.',
                        settings.EMAIL_HOST_USER,
                        [item['mailCont']],
                        fail_silently=False,
                        connection=connection
                          )
            else:
                GestoresCreationRequest.objects.create(
                    email=item['mailCont'],
                    data = {
                        'NombreCompleto': item['nomCont'],
                        'Telefono': '',
                        'Cta': cta,
                        'TipoUsuario': item['tipoCont'],
                        'ref': item['idCliente'],
                        'email': item['mailCont'],
                        'empresa': nombre
                    },
                    token=token
                )
        data = {
            "success": True,
            "message": "Solicitud de registro creada exitosamente. Revisa tu correo para completar el proceso.",
            "ref": "Success"
        }
        return data
