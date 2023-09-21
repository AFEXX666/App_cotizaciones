import requests
from bs4 import BeautifulSoup
import urllib.parse
from werkzeug.security import check_password_hash

def get_image_url(name):
    API_KEY = 'AIzaSyBsO-8A8qtM41tOKuZ07iTXimtq5AeQpJs'
    SEARCH_ENGINE_ID = '21a2bf56b1ed44b37'
    
    words_to_remove = ['Multiplataforma', 'Área', 'Area', 'de', 'y', 'Negocios', 'Digitales', 'Eficientes']
    
    # Eliminar las palabras de la consulta
    for word in words_to_remove:
        name = name.replace(word, '')
    
    encoded_query = urllib.parse.quote(name)
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={encoded_query}&searchType=image"
    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        image_url = data['items'][0]['link']
    else:
        # Si no se encuentra ninguna imagen, puedes proporcionar una URL de imagen alternativa
        image_url = "URL_DE_IMAGEN_ALTERNATIVA"

    return image_url
