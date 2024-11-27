from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rapidoysabrosoWEB.models import Mapa_data, Url_Locales
import os
import django

class Command(BaseCommand):
    help = 'Extrae datos de las URLs de la base de datos y los guarda en la base de datos'

    def handle(self, *args, **kwargs):
        # Configura las opciones de Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecuta en modo sin ventana
        chrome_options.add_argument("--disable-gpu")  # Recomendado para headless
        chrome_options.add_argument("--no-sandbox")  # Por compatibilidad

        # Ruta al ChromeDriver
        chrome_service = Service(r"C:\SeleniumDrivers\chromedriver.exe")  # Ajusta la ruta aquí

        # Inicializa el navegador
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        # Obtener todas las URLs de la base de datos
        urls = Url_Locales.objects.all()  # Puedes agregar filtros si lo deseas, por ejemplo, limitando a ciertas URLs

        # Iterar sobre cada URL en la base de datos
        for url_obj in urls:
            url = url_obj.url
            self.stdout.write(self.style.NOTICE(f"Procesando URL: {url}"))

            try:
                # Cargar la página
                driver.get(url)

                # Usar WebDriverWait para esperar explícitamente que el contenedor con la clase aparezca
                try:
                    # Esperar hasta que el contenedor con la clase 'p_yaB_HV2WHmVqYhD9eFG' esté presente en el DOM
                    containers = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "p_yaB_HV2WHmVqYhD9eFG"))
                    )

                    # Iterar sobre los contenedores encontrados
                    for container in containers:
                        # Buscar el h3 dentro de cada contenedor (Local)
                        h3_element = container.find_element(By.TAG_NAME, "h3")
                        local = h3_element.text.strip()

                        # Buscar los a con la clase '_23zkYzJmHt5A4mqX11HBiL' dentro del contenedor
                        a_elements = container.find_elements(By.CSS_SELECTOR, "a._23zkYzJmHt5A4mqX11HBiL")

                        direccion = ""
                        coordenadas = ""

                        if a_elements:
                            # Dirección: Obtener el primer href (asumimos que es la dirección)
                            direccion_url = a_elements[0].get_attribute('href')

                            # Extraer las coordenadas después del '='
                            if '=' in direccion_url:
                                coordenadas = direccion_url.split('=')[1]  # Extraer las coordenadas

                            if len(a_elements) > 1:
                                # Obtener el texto del segundo href (dirección física completa)
                                direccion = a_elements[1].text.strip()

                        # Crear y guardar la entrada en la base de datos (Modelo Mapa_data)
                        # Crear el objeto Mapa_data
                        Mapa_data.objects.create(
                            local=local,  # Local desde h3
                            direccion=direccion,  # Dirección desde el texto del segundo href
                            coordenadas=coordenadas,  # Coordenadas extraídas de la URL
                            url=url_obj,  # Relación con el objeto URL
                        )

                    self.stdout.write(self.style.SUCCESS(f"Datos guardados exitosamente para {url}."))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"No se pudo procesar el contenedor de la URL {url}. Error: {e}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"No se pudo cargar la URL {url}. Error: {e}"))

        # Cierra el navegador después de terminar
        driver.quit()
