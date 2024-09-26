from django.shortcuts import render, redirect
from django.urls import path, include
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
from lxml import html
import json
import time

# Configuración global para la API de pedidos
GET_MENUS = "https://www.pedidosya.cl/home-page/v32/home/lazy_load?country_id=2&area_id=16977&lat=-33.44889&lng=-70.669266&in_progress_order=false&alchemist_one_enabled=false&component_suffix=_v2"

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-419,es;q=0.9',
    'baggage': 'sentry-environment=live,sentry-release=peya-web%403.0.19,sentry-public_key=b015b29cb0524fa6a58705cc439e4075,sentry-trace_id=1417b628529b4cab87eaf4de815e6bb7,sentry-sample_rate=0.1,sentry-sampled=true',
    'cache-control': 'no-cache',
    'home-platform': 'desktop',
    'priority': 'u=1, i',
    'referer': 'https://www.pedidosya.cl/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

# Vistas de autenticación
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
    return render(request, 'service/menu.html')

def logout_view(request):
    logout(request)
    return redirect('vista1')


# Función para extraer URLs y IDs de la respuesta JSON
def extract_target_urls(data):
    print("extract_target_urls llamado")
    urls = []
    id_list = []
    
    # Recorrer la estructura JSON para extraer URLs e IDs
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
    
    print("URLs extraídas:", urls)
    print("IDs extraídos:", id_list)
    return [url for url in urls if url], [rid for rid in id_list if rid]

# Función para obtener todos los menús
def get_all_menus(urls, id_list):
    url_pedidos_ya_bk = "https://www.pedidosya.cl/v2/niles/partners/{id}/menus?isJoker=false&occasion=DELIVERY"
    
    headers['referer'] = 'https://www.pedidosya.cl/'  # Asegurarse de enviar el 'referer' correcto
    list_total = []

    for refer, restaurant_id in zip(urls, id_list):
        complete_url = f"https://www.pedidosya.cl/{refer}"
        rest_name = str(refer).split('/')[-1].replace('-', ' ').upper()
        
        headers['referer'] = complete_url
        response = requests.get(url_pedidos_ya_bk.format(id=restaurant_id), headers=headers)
        
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

        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error al procesar datos para el restaurante {rest_name}: {e}")
        
        time.sleep(3)  # Control de tasa de peticiones para evitar ser bloqueado por la API

    print("get_all_menus llamado")
    print("URLs recibidas:", urls)
    print("IDs recibidas:", id_list)
    
    return list_total

# Vista principal que gestiona el proceso de extracción de menús y los renderiza en el HTML
def menu_view(request):
    try:
        # Hacer la solicitud a la API de PedidosYa
        response = requests.get(GET_MENUS, headers=headers)
        print("Código de estado de la respuesta:", response.status_code)
        print("Contenido crudo de la respuesta:", response.text)  # Verificar si se obtiene la respuesta adecuada
        
        if response.status_code == 200:
            menus_js = json.loads(response.text)
            target_urls, id_lst = extract_target_urls(menus_js)
            menus = get_all_menus(target_urls, id_lst)
            print(menus)  # Imprimir los menús extraídos para depuración

        else:
            menus = []
            print(f"Error en la solicitud a la API: {response.status_code}")

    except requests.RequestException as e:
        print("Error en la petición:", e)
        menus = []

    # Renderizar los menús en la plantilla
    return render(request, 'service/promotions.html', {'menus': menus})