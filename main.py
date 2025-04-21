from auth.login import login_SRI
from scraper.navigate import navegar_comprobantes
from scraper.menu_usuario import seleccionar_fecha, seleccionar_comprobante, automatizar_seleccion
from scraper.downloader import descargar_comprobantes_txt, descargar_xml

import time

def descargar_comprobantes(pagina):
    try:
        if navegar_comprobantes(pagina):
            year, mes = seleccionar_fecha()
            comprobante_valor, comprobante_nombre = seleccionar_comprobante()
            
            print(f"\nSimulando la seleccion de busqueda de comprobantes tipo {comprobante_nombre} de {mes} - {year}")
            automatizar_seleccion(year, mes, comprobante_valor, pagina)
            descargar_comprobantes_txt(pagina, comprobante_nombre.replace(" ", "_"), mes, year)
            
            descargar_xml(pagina, comprobante_nombre.replace(" ", "_"),  mes, year)
            
            return True
        else: 
            print("No se pudo acceder a la sección de comprobantes.")
            return False
    except Exception as e:
        print(f"Error al descargar los comprobantes: {e}")
        return False


def main():
    try:
        print("Iniciando sesion en el SRI...")
        login_SRI(descargar_comprobantes) # Ejecut la funcion de login
    except Exception as e:
        print(f"Error en main: {e}")

main()