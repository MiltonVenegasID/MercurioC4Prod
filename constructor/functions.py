import os
from dotenv import load_dotenv
import requests
load_dotenv()

def hub_register(correo, cuenta):
    api = os.getenv('API_HUB')
    id_rec = os.getenv('API_ID_CHECK')
    recovered_id = requests.get(id_rec + cuenta)
    if recovered_id == '':
        return "no"
    else:
        return "si"
