from django.shortcuts import render
from django.urls import path , include
import requests
from lxml import html
import requests
import json


encabezado = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def vista1(request):


    # ##url = "https://www.wikipedia.org"
    # url = "https://www.pedidosya.cl/restaurantes/santiago/burger-king-los-heroes-menu?search=burger%20king"



    # respuesta = requests.get(url, headers = encabezado)

    # parser = html.fromstring(respuesta.text)

    # #titulo = parser.get_element_by_id("js-link-box-en") #busca x ID#

    # #print (titulo.text_content()) #.text_content para obtener texto de la etiqueta#

    # hambrugesas = parser.find_class('sc-72orc4-1 sc-byqjo7-0 fImiFL gLYqNM')

    # for hamburguesa in hambrugesas: 
    #     print(hamburguesa.text_content())

    # #----------------------------------------------------------------------------------#
    # #CODIGO TRAE TODOS LOS NOMBRES DEL MENU POR XPATH PERSONALIZADO#

    # # hamburguesas = parser.xpath("//div[@class='col-sm-4 col-md-4 col-6']//h4/text()")

    # # for hamburguesa in hamburguesas: 
    # #     print(hamburguesa)

    # #-----------------------------------------------------------------------------------#





    return render(request,'service/vista1.html')

def vistaBk(request):

    url = "https://www.pedidosya.cl/v2/niles/partners/66202/menus?isJoker=false&occasion=DELIVERY"

    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-419,es;q=0.9',
    'cookie': '__Secure-peya.sid=s%3A8adc0b39-e29d-429e-910e-f6642d632545.%2BkiknsnQQFekfrWbe2kb411POh6pU8B7UrzXa2krcpo; __Secure-peyas.sid=s%3Ab1db62b8-b06b-4853-a7f3-d9c27e73f804.RnjXlKMBo5It882wb9rxRKWmnwiPL%2BJP94QqzDw26QQ; _pxhd=Nlpy1nKdaUOXPq3FqLlj5IFOLz2hsd9dODvRQtHJ8B5UH-Kr/n-Oxky97gLlP-2dtttDMAzVpY8A7BQ0OhtxaQ==:as5--a7MqYbyKWZEh5LKc-wJKp2x4Nn3ux0J-jD5NfoPZA3uvXz4Lii3jvwfgZdpyK9LyHZxiO7aeNo/4u5YUP3YqYV0RRlIg6l6grNdy9E=; __cf_bm=tmizSII3dJhorQTxPCEf.Z9tafXxKmh9W9_nI77oTRc-1725317015-1.0.1.1-5kR0s9M_ssGKHlrSmKAoVfgHdCPV7wz5JbWY6yi1AuMuY8bf5t_qWAeo3CBZogXEBucDHRz4GvTnAfjobSofqg; pxcts=cabf33ba-697c-11ef-b4ba-2c8f50230aad; _pxvid=c012911e-697b-11ef-86d6-398b5580b95a; _gcl_au=1.1.2142199783.1725317019; dhhPerseusSessionId=1725317033261.000000004269648352.0001s3iv2y; dhhPerseusGuestId=1725317033261.000000002060059593.0000md2pcf; ab.storage.userId.8f8614b7-a682-4b80-af4e-c133abb05875=%7B%22g%22%3A%22%5Bobject%20Object%5D%22%2C%22c%22%3A1725317019369%2C%22l%22%3A1725317019371%7D; ab.storage.deviceId.8f8614b7-a682-4b80-af4e-c133abb05875=%7B%22g%22%3A%224076a6da-04fc-add5-7017-54698b6381ff%22%2C%22c%22%3A1725317019372%2C%22l%22%3A1725317019372%7D; _fbp=fb.1.1725317019712.706598983938978389; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1620376049.1725317023; _gat_WD2_Tracker_PeYa_Prod=1; _px3=4f43c262a00c37acb5b18015a0fe0dc4a379345bbebff9da353ae837b77c1ea1:0D0LM8EPdn4QlJZoddm+OMWxMb/xENdUaOxQSaPEUvC8rv3oP7HasiJ8lJJSd1h57eVs1WO7yfjIYciZT8FdkA==:1000:mfaXu+7cw7VVAqcP6QtXPsv4BA37GM0+RinD+HjYXiF8vjQJsuy/bNQJ6R0okS3VYOEaSh+gK40vzx9YPld9UPB1tWqRtda7qzj2fTN3gvu4qCPQgsKjIdKHMJcs88wbpYw67sA94y4rTGgoVPDxnyDD2JtswMWzWkPuByEWztqEdCKeAlBDEitUi55/l0/TKhe5nmTuEquD7DLxByOiMi4/0B0RFeS9mrcNYo9XTu8=; _ga_LQWR31SY8G=GS1.1.1725317019.1.1.1725317042.37.0.0; _ga=GA1.2.1380648260.1725317020; _tq_id.TV-81819090-1.cd2b=bda1feaaf9c57667.1725317021.0.1725317042..; ab.storage.sessionId.8f8614b7-a682-4b80-af4e-c133abb05875=%7B%22g%22%3A%22db1d810e-44ac-ab60-8327-b639ae23dcd3%22%2C%22e%22%3A1725318842230%2C%22c%22%3A1725317019370%2C%22l%22%3A1725317042230%7D; _uetsid=cdc26960697c11efb016c99f0bb472d8; _uetvid=cdc27980697c11efaef2cd4c5b199f57; dhhPerseusHitId=1725317057543.000000000220935440.0000ktzbwp; __cf_bm=sfJzVI4AoRA23uQNeO0pZFWZJboH81JP25fnXU5Yy0o-1725317181-1.0.1.1-OVxlXa1n7xZ0c3MmlZBeFgdF1Zn9Rs6RUQkBz_JMHh_4IIdeuFUw3P43zay9jcxIUsV55G6xGZcO4udO4qnR0g; __Secure-peya.sid=s%3A8adc0b39-e29d-429e-910e-f6642d632545.%2BkiknsnQQFekfrWbe2kb411POh6pU8B7UrzXa2krcpo; __Secure-peyas.sid=s%3Ab1db62b8-b06b-4853-a7f3-d9c27e73f804.RnjXlKMBo5It882wb9rxRKWmnwiPL%2BJP94QqzDw26QQ',
    'priority': 'u=1, i',
    'referer': 'https://www.pedidosya.cl/restaurantes/santiago/burger-king-los-heroes-menu?search=burger%20king',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    json_response = json.loads(response.text)
    object_list = []
    list_total = []
    prices = []


    for item in json_response['sections']:
        name = item['name']
        object_list = [] 

        for i, product in enumerate(item['products']):
            if i >= 5:  # Limitar a 5 productos
                break

            description = product['description']
            price = product['price']['finalPrice']
            obj = {
                'description': description,
                'price': price
            }
            object_list.append(obj)

        object_info = {
            'promo': name,
            'details': object_list
        }
        list_total.append(object_info)

    # printear valores por indice
    if list_total and list_total[0]['details']:
        print(f"La promo '{list_total[0]['promo']}' tiene un valor de {list_total[0]['details'][0]['price']} CLP")
    else:
        print("No hay productos en la primera promoción.")

    # printear valores por el valor de alguna key como la promo
    promo_name_to_find = 'Los Favoritos de Bk!'
    for promo in list_total:
        if promo['promo'] == promo_name_to_find:
            if promo['details']:
                first_product = promo['details'][0]
                print(f"El primer producto en la promoción '{promo_name_to_find}' tiene un precio de {first_product['price']}")
            else:
                print(f"La promoción '{promo_name_to_find}' no tiene productos.")
            break
    else:
        print(f"No se encontró la promoción '{promo_name_to_find}' en la lista.")


    context = {
        'promotions': list_total
    }
    
    return render(request, 'service/burgerk.html', context)



def mcdonals(request):
    url = "https://www.pedidosya.cl/v2/niles/partners/66202/menus?isJoker=false&occasion=DELIVERY"



    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-419,es;q=0.9',
    'cookie': '__Secure-peya.sid=s%3A8adc0b39-e29d-429e-910e-f6642d632545.%2BkiknsnQQFekfrWbe2kb411POh6pU8B7UrzXa2krcpo; __Secure-peyas.sid=s%3Ab1db62b8-b06b-4853-a7f3-d9c27e73f804.RnjXlKMBo5It882wb9rxRKWmnwiPL%2BJP94QqzDw26QQ; _pxhd=Nlpy1nKdaUOXPq3FqLlj5IFOLz2hsd9dODvRQtHJ8B5UH-Kr/n-Oxky97gLlP-2dtttDMAzVpY8A7BQ0OhtxaQ==:as5--a7MqYbyKWZEh5LKc-wJKp2x4Nn3ux0J-jD5NfoPZA3uvXz4Lii3jvwfgZdpyK9LyHZxiO7aeNo/4u5YUP3YqYV0RRlIg6l6grNdy9E=; __cf_bm=tmizSII3dJhorQTxPCEf.Z9tafXxKmh9W9_nI77oTRc-1725317015-1.0.1.1-5kR0s9M_ssGKHlrSmKAoVfgHdCPV7wz5JbWY6yi1AuMuY8bf5t_qWAeo3CBZogXEBucDHRz4GvTnAfjobSofqg; pxcts=cabf33ba-697c-11ef-b4ba-2c8f50230aad; _pxvid=c012911e-697b-11ef-86d6-398b5580b95a; _gcl_au=1.1.2142199783.1725317019; dhhPerseusSessionId=1725317033261.000000004269648352.0001s3iv2y; dhhPerseusGuestId=1725317033261.000000002060059593.0000md2pcf; ab.storage.userId.8f8614b7-a682-4b80-af4e-c133abb05875=%7B%22g%22%3A%22%5Bobject%20Object%5D%22%2C%22c%22%3A1725317019369%2C%22l%22%3A1725317019371%7D; ab.storage.deviceId.8f8614b7-a682-4b80-af4e-c133abb05875=%7B%22g%22%3A%224076a6da-04fc-add5-7017-54698b6381ff%22%2C%22c%22%3A1725317019372%2C%22l%22%3A1725317019372%7D; _fbp=fb.1.1725317019712.706598983938978389; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1620376049.1725317023; _gat_WD2_Tracker_PeYa_Prod=1; _px3=4f43c262a00c37acb5b18015a0fe0dc4a379345bbebff9da353ae837b77c1ea1:0D0LM8EPdn4QlJZoddm+OMWxMb/xENdUaOxQSaPEUvC8rv3oP7HasiJ8lJJSd1h57eVs1WO7yfjIYciZT8FdkA==:1000:mfaXu+7cw7VVAqcP6QtXPsv4BA37GM0+RinD+HjYXiF8vjQJsuy/bNQJ6R0okS3VYOEaSh+gK40vzx9YPld9UPB1tWqRtda7qzj2fTN3gvu4qCPQgsKjIdKHMJcs88wbpYw67sA94y4rTGgoVPDxnyDD2JtswMWzWkPuByEWztqEdCKeAlBDEitUi55/l0/TKhe5nmTuEquD7DLxByOiMi4/0B0RFeS9mrcNYo9XTu8=; _ga_LQWR31SY8G=GS1.1.1725317019.1.1.1725317042.37.0.0; _ga=GA1.2.1380648260.1725317020; _tq_id.TV-81819090-1.cd2b=bda1feaaf9c57667.1725317021.0.1725317042..; ab.storage.sessionId.8f8614b7-a682-4b80-af4e-c133abb05875=%7B%22g%22%3A%22db1d810e-44ac-ab60-8327-b639ae23dcd3%22%2C%22e%22%3A1725318842230%2C%22c%22%3A1725317019370%2C%22l%22%3A1725317042230%7D; _uetsid=cdc26960697c11efb016c99f0bb472d8; _uetvid=cdc27980697c11efaef2cd4c5b199f57; dhhPerseusHitId=1725317057543.000000000220935440.0000ktzbwp; __cf_bm=sfJzVI4AoRA23uQNeO0pZFWZJboH81JP25fnXU5Yy0o-1725317181-1.0.1.1-OVxlXa1n7xZ0c3MmlZBeFgdF1Zn9Rs6RUQkBz_JMHh_4IIdeuFUw3P43zay9jcxIUsV55G6xGZcO4udO4qnR0g; __Secure-peya.sid=s%3A8adc0b39-e29d-429e-910e-f6642d632545.%2BkiknsnQQFekfrWbe2kb411POh6pU8B7UrzXa2krcpo; __Secure-peyas.sid=s%3Ab1db62b8-b06b-4853-a7f3-d9c27e73f804.RnjXlKMBo5It882wb9rxRKWmnwiPL%2BJP94QqzDw26QQ',
    'priority': 'u=1, i',
    'referer': '"https://www.pedidosya.cl/restaurantes/santiago/mcdonalds-republica-f40243b1-de54-4b6e-82e8-90facde70842-menu"',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }


    response = requests.request("GET", url, headers=headers, data=payload)

    json_response = json.loads(response.text)
    object_list = []
    list_total = []
    prices = []


    for item in json_response['sections']:
        name = item['name']
        object_list = [] 

        for i, product in enumerate(item['products']):
            if i >= 5:  # Limitar a 5 productos
                break

            description = product['description']
            price = product['price']['finalPrice']
            obj = {
                'description': description,
                'price': price
            }
            object_list.append(obj)

        object_info = {
            'promo': name,
            'details': object_list
        }
        list_total.append(object_info)


    context = {
        'promotions': list_total
    }

    return render(request, 'service/mcdonals.html', context)