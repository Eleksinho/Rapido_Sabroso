from django.shortcuts import render, redirect
from django.urls import path, include
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse

from lxml import html
import requests
import json
import time
import random
from bs4 import BeautifulSoup

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

# Vista de autenticación
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

# Función para extraer URLs e IDs del JSON
def extract_target_urls(data, max_depth=10, max_urls=50, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    if current_depth > max_depth:
        return [], []

    urls = []
    id_list = []

    if isinstance(data, dict):
        actions = data.get('actions', [])
        if actions:
            for action in actions:
                if 'target_url' in action:
                    target_url = action.get('target_url')
                    rest_id = data.get('id', '')
                    
                    if target_url and target_url not in visited and len(urls) < max_urls:
                        urls.append(target_url)
                        id_list.append(rest_id)
                        visited.add(target_url)

        for key, value in data.items():
            if isinstance(value, (dict, list)):
                new_urls, new_ids = extract_target_urls(value, max_depth, max_urls, current_depth + 1, visited)
                urls.extend(new_urls)
                id_list.extend(new_ids)

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                new_urls, new_ids = extract_target_urls(item, max_depth, max_urls, current_depth + 1, visited)
                urls.extend(new_urls)
                id_list.extend(new_ids)

    return list(set(urls)), list(set(id_list))

# Función para obtener todos los menús


# Función para obtener todos los menús
def get_all_menus(urls, id_list, max_requests=10):
    print('Entrando en get_all_menus')
    url_pedidos_ya_bk = "https://www.pedidosya.cl/v2/niles/partners/{id}/menus?isJoker=false&occasion=DELIVERY"
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
        'sentry-trace': '1417b628529b4cab87eaf4de815e6bb7-ba6163f05744f123-1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'
    }
    processed_requests = 0

    for refer, restaurant_id in zip(urls, id_list):
        print(f'Procesando restaurante: {restaurant_id}')
        if processed_requests >= max_requests:
            print('Límite de solicitudes alcanzado')
            break

        complete_url = f"https://www.pedidosya.cl/{refer}"
        rest_name = str(refer).split('/')[-1].replace('-', ' ').upper()
        headers['referer'] = complete_url

        response = requests.get(
            url_pedidos_ya_bk.format(id=restaurant_id),
            headers=headers,
            timeout=10
        )
        print(f"HTTP Status: {response.status_code}")

        try:
            print("entra al producto")
            json_response = json.loads(response.text)
            for item in json_response.get('sections', []):
                name = item['name']
                object_list = []

                for i, product in enumerate(item['products']):
                    print("revisa los productos")
                    if i >= 5:
                        break
                    description = product.get('description', '')
                    price = product.get('price', {}).get('finalPrice', 'N/A')
                    object_list.append({'description': description, 'price': price})
                    print(f'Producto encontrado: {description} - {price}')
                
                # Yield el menú en lugar de almacenarlo en una lista
                yield {'restaurant': rest_name, 'promo': name, 'details': object_list}

            processed_requests += 1

        except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
            print(f"Error al procesar datos para el restaurante {rest_name}: {e}")

        time.sleep(random.uniform(2, 5))


# Vista principal que gestiona el proceso de extracción de menús
def menu_index(request):
    return render(request, 'service/promotions.html')

def menu_view(request):
    def stream_menus():
        try:
            response = requests.get(GET_MENUS, headers=headers, timeout=10)
            if response.status_code == 200:
                menus_js = json.loads(response.text)
                target_urls, id_lst = extract_target_urls(menus_js)
                
                # Comienza el streaming de los menús obtenidos
                yield '{"menus": ['

                first = True  # Para manejar la coma entre los elementos
                for menu in get_all_menus(target_urls, id_lst, max_requests=10):
                    if not first:
                        yield ','  # Separador entre los elementos
                    yield json.dumps(menu)
                    first = False

                yield ']}'  # Cierra el JSON

            else:
                yield '{"error": "Error en la solicitud a la API"}'

        except requests.RequestException as e:
            yield '{"error": "Error en la petición a la API"}'

    # Usar StreamingHttpResponse para devolver los menús mientras se procesan
    return StreamingHttpResponse(stream_menus(), content_type='application/json')



#PLAAAN BBBBBBB#

import requests
from lxml import html

def obtener_productos():
    url = "https://www.wendys.cl/pedir"
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'es-419,es;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parsear el contenido HTML
        tree = html.fromstring(response.content)

        # Usar XPath para extraer los productos
        productos = []
        contenedores_productos = tree.xpath('//div[@class="flex flex-col justify-between h-40 w-[60%] sm:w-56 p-3.5 pr-3"]')

        for producto in contenedores_productos:
            # Extraer el nombre del producto
            nombre = producto.xpath('.//span[@class="line-clamp-2"]/text()')[0].strip() if producto.xpath('.//span[@class="line-clamp-2"]/text()') else 'Nombre no disponible'
            
            # Extraer la descripción del producto
            descripcion = producto.xpath('.//p[@class="mt-0.5 text-xs text-ellipsis dark:text-neutral-300 whitespace-pre-wrap line-clamp-3"]/text()')[0].strip() if producto.xpath('.//p[@class="mt-0.5 text-xs text-ellipsis dark:text-neutral-300 whitespace-pre-wrap line-clamp-3"]/text()') else 'Descripción no disponible'
            
            # Extraer el precio del producto
            precio = producto.xpath('.//div[@class="flex gap-x-2 text-sm flex-row"]/div/text()')[0].strip() if producto.xpath('.//div[@class="flex gap-x-2 text-sm flex-row"]/div/text()') else 'Precio no disponible'
            
            # Inicializa la URL de imagen como una cadena vacía (ajusta esto si hay imágenes disponibles)
            imagen_url = ''  # Si hay imágenes, ajusta esta línea para extraerlas

            # Añadir el producto a la lista
            productos.append({
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'imagen_url': imagen_url
            })

        return productos
    else:
        print(f"Error al obtener la página: {response.status_code}")
        return []

from django.shortcuts import render

def menu(request):
    productos = obtener_productos()  # Obtener los productos mediante la función de scraping
    context = {
        'productos': productos
    }
    return render(request, 'service/menu.html', context)