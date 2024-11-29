from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rapidoysabrosoWEB.models import Mapa_data, Url_Locales, Marca
from django.db import IntegrityError
from urllib.parse import urlparse

def obtener_marca(url):
    dominio = urlparse(url).netloc
    return dominio.split('.')[1] if '.' in dominio else dominio

class Command(BaseCommand):
    help = 'Extrae datos de las URLs usando selectores fijos y guarda los resultados en la base de datos'

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
        urls = Url_Locales.objects.all()

        for url_obj in urls:
            url = url_obj.url
            self.stdout.write(self.style.NOTICE(f"Procesando URL: {url}"))

            try:
                # Cargar la página
                driver.get(url)

                try:
                    # Esperar hasta que los contenedores estén presentes
                    containers = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "p_yaB_HV2WHmVqYhD9eFG"))
                    )

                    # Procesar cada contenedor
                    for container in containers:
                        # Local
                        h3_element = container.find_element(By.TAG_NAME, "h3")
                        local = h3_element.text.strip()

                        # Dirección y teléfono
                        a_elements = container.find_elements(By.CSS_SELECTOR, "a._23zkYzJmHt5A4mqX11HBiL")
                        direccion = ""
                        telefono = ""
                        coordenadas = ""

                        if a_elements:
                            # Dirección: Extraer del texto del primer enlace
                            direccion = a_elements[0].text.strip()

                            # Extraer las coordenadas de la URL (después del '=')
                            direccion_url = a_elements[0].get_attribute("href")
                            if "=" in direccion_url:
                                coordenadas = direccion_url.split("=")[-1]  # Coordenadas lat, long

                            # Teléfono: Extraer del segundo enlace si existe
                            if len(a_elements) > 1:
                                telefono_href = a_elements[1].get_attribute("href")
                                if "tel:" in telefono_href:
                                    telefono = telefono_href.split("tel:")[1]

                        # Obtener el nombre de la marca desde la URL
                        marca_nombre = obtener_marca(url)

                        # Buscar la marca en la base de datos
                        marca = Marca.objects.filter(nombre__iexact=marca_nombre).first()

                        if not marca:
                            self.stdout.write(self.style.ERROR(f"No se encontró la marca '{marca_nombre}' en la base de datos."))
                            continue  # Si no se encuentra la marca, saltamos a la siguiente URL

                        # Intentar obtener el objeto Mapa_data existente o crearlo
                        try:
                            mapa_data, created = Mapa_data.objects.update_or_create(
                                local=local,
                                direccion=direccion,
                                defaults={
                                    'telefono': telefono,
                                    'coordenadas': coordenadas,  # Coordenadas extraídas de la URL
                                    'Marca': marca,
                                    'fuente_url_mapa': url_obj,
                                }
                            )

                            if created:
                                self.stdout.write(self.style.SUCCESS(f"Datos guardados para {local}"))
                            else:
                                self.stdout.write(self.style.SUCCESS(f"Datos actualizados para {local}"))

                        except IntegrityError as e:
                            self.stdout.write(self.style.ERROR(f"Error al guardar los datos de {local}: {e}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error al procesar los contenedores en la URL {url}: {e}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"No se pudo cargar la URL {url}: {e}"))
                continue  # Continúa con la siguiente URL si hay un error

        # Cerrar el navegador después de completar el proceso
        driver.quit()
