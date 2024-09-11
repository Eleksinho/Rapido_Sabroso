from django.shortcuts import render , redirect
from django.urls import path , include
import requests
from lxml import html
import requests
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import time

def vista1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu') 
        else:
            error_message = 'Usuario o contraseña incorrectos.'
            return render(request, 'service/vista1.html', {'error_message': error_message})
    
 
    return render(request, 'service/vista1.html')


def menu(request):
    return render(request , 'service/menu.html')

#Cerrar sesion#
def logout_view(request):
    logout(request)
    return redirect('vista1')

# Configuración global
GET_MENUS = "https://www.pedidosya.cl/home-page/v32/home/lazy_load?country_id=2&area_id=16977&lat=-33.44889&lng=-70.669266&in_progress_order=false&alchemist_one_enabled=false&component_suffix=_v2"

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-419,es;q=0.9',
    'baggage': 'sentry-environment=live,sentry-release=peya-web%403.0.19,sentry-public_key=b015b29cb0524fa6a58705cc439e4075,sentry-trace_id=1417b628529b4cab87eaf4de815e6bb7,sentry-sample_rate=0.1,sentry-sampled=true',
    'cache-control': 'no-cache',
    'cookie': '',
    'home-platform': 'desktop',
    'priority': 'u=1, i',
    'referer': 'https://www.pedidosya.cl/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '1417b628529b4cab87eaf4de815e6bb7-ba6163f05744f123-1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

import requests
import json
import time

# URL de la API de pedidos
GET_MENUS = "https://www.pedidosya.cl/home-page/v32/home/lazy_load?country_id=2&area_id=16977&lat=-33.44889&lng=-70.669266&in_progress_order=false&alchemist_one_enabled=false&component_suffix=_v2"

# Configuración para la petición
payload = {}
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-419,es;q=0.9',
    'baggage': 'sentry-environment=live,sentry-release=peya-web%403.0.19,sentry-public_key=b015b29cb0524fa6a58705cc439e4075,sentry-trace_id=1417b628529b4cab87eaf4de815e6bb7,sentry-sample_rate=0.1,sentry-sampled=true',
    'cache-control': 'no-cache',
    'cookie': '',
    'home-platform': 'desktop',
    'priority': 'u=1, i',
    'referer': 'https://www.pedidosya.cl/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '1417b628529b4cab87eaf4de815e6bb7-ba6163f05744f123-1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

# Obtener los menús
response = requests.request("GET", GET_MENUS, headers=headers, data=payload)
menus_js = json.loads(response.text)

# Función para obtener todos los menús
# Modifica la función `get_all_menus` para devolver los datos
def get_all_menus(urls, id_list):
    url_pedidos_ya_bk = "https://www.pedidosya.cl/v2/niles/partners/{id}/menus?isJoker=false&occasion=DELIVERY"
    payload = {}
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'es-419,es;q=0.9',
        'cookie': '',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    list_total = []

    for refer, restaurant_id in zip(urls, id_list):
        complete_url = f"https://www.pedidosya.cl/{refer}"
        rest_name = str(refer).split('/')[-1].replace('-', ' ').upper()

        headers['referer'] = complete_url
        response = requests.request("GET", url_pedidos_ya_bk.format(id=restaurant_id), headers=headers, data=payload)
        
        try:
            json_response = json.loads(response.text)
            for item in json_response.get('sections', []):
                name = item['name']
                object_list = []

                # Limitar a 5 productos
                for i, product in enumerate(item['products']):
                    if i >= 5:
                        break
                    description = product.get('description', '')
                    price = product.get('price', {}).get('finalPrice', 'N/A')
                    object_list.append({'description': description, 'price': price})

                list_total.append({'restaurant': rest_name, 'promo': name, 'details': object_list})

        except KeyError:
            print(f"No se encontraron 'sections' para el restaurante {rest_name}")
        time.sleep(3)

    return list_total


# Función para extraer URLs y IDs
def extract_target_urls(data):
    urls = []
    id_list = []

    if isinstance(data, dict):
        if 'actions' in data:
            for action in data['actions']:
                if 'target_url' in action:
                    urls.append(action['target_url'])
                    id_list.append(data.get('id', ''))

        for value in data.values():
            new_urls, new_ids = extract_target_urls(value)
            urls.extend(new_urls)
            id_list.extend(new_ids)

    elif isinstance(data, list):
        for item in data:
            new_urls, new_ids = extract_target_urls(item)
            urls.extend(new_urls)
            id_list.extend(new_ids)

    return [url for url in urls if url], [rid for rid in id_list if rid]

# Extraer las URLs y las IDs
target_urls, id_lst = extract_target_urls(menus_js)

# Ejecutar la función para obtener menús
get_all_menus(target_urls, id_lst)

def menu_view(request):
    target_urls, id_lst = extract_target_urls(menus_js)
    menus = get_all_menus(target_urls, id_lst)
    return render(request, 'service/promotions.html', {'menus': menus})