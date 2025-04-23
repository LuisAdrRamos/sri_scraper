from auth.login import login_SRI
from scraper.navigate import navegar_comprobantes
from scraper.downloader import automatizar_y_descargar
import os

def descargar_comprobantes(pagina):
    try:
        if navegar_comprobantes(pagina):
            print("\nIniciando descarga automática de comprobantes...")
            automatizar_y_descargar(pagina)
            return True
        else:
            print("No se pudo acceder a la sección de comprobantes.")
            return False
    except Exception as e:
        print(f"Error al descargar los comprobantes: {e}")
        return False

def main():
    try:
        print("Iniciando sesión en el SRI...")
        login_SRI(descargar_comprobantes)
    except Exception as e:
        print(f"Error en main: {e}")

if __name__ == "__main__":
    main()