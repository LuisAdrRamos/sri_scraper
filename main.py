from auth.login import login_SRI
from scraper.navigate import navegar_comprobantes
from scraper.downloader import automatizar_y_descargar

from processor.proceso_facturas_xml import generar_archivo_detalles_productos
from processor.proceso_retencion_xml import generar_archivo_detalles_retenciones
from processor.proceso_creditos_xml import generar_archivo_detalles_notas_credito

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
        
        print("Procesando los archivos de facturas")
        generar_archivo_detalles_productos()
        
        print("Procesando los archivos de retencion")
        generar_archivo_detalles_retenciones()
        
        print("Procesando los archivos de credito")
        generar_archivo_detalles_notas_credito()
    except Exception as e:
        print(f"Error en main: {e}")

main()