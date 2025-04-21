from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time

# Carga las variables de entorno
load_dotenv()

# Lee las credenciales del contribuyente desde el .env
RUC = os.getenv("SRI_RUC")
PASSWORD = os.getenv("SRI_PASSWORD")

def login_SRI(descarga_callback):
    try:
        with sync_playwright() as login:

            # Crear el navegador
            navegador = login.chromium.launch(headless=False)
            contexto = navegador.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            )

            pagina = contexto.new_page()

            # Navega hasta la URL de login del SRI
            pagina.goto("https://srienlinea.sri.gob.ec/sri-en-linea/contribuyente/perfil")

            # Llena el input del RUC y Contraseña
            pagina.fill("input#usuario", RUC)
            pagina.fill("input#password", PASSWORD)

            # Hace click en el boton de ingresar
            pagina.click("input#kc-login")

            # Esperar unos segundos para verificar que la página ha cargado
            pagina.wait_for_load_state("load")  # Esperar que cargue la página
            print("Inicio de sesión exitoso.")
            
            descarga_completa = descarga_callback(pagina)
            
            if descarga_completa:
                print("Todos los comprobantes han sido descargados")
            else:
                print("No se pudo completar la descarga")
            time.sleep(2)

    except TimeoutError: 
        print("Error al iniciar sesion")
    except Exception as e:
        print(f"Error inseperado: {e}")
    finally:
        navegador.close
        print("El navegador se a cerrado")


if __name__ == "main":
    login_SRI()