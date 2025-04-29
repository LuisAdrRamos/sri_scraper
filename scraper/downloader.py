import os
from pathlib import Path
from playwright.sync_api import Page

# Diccionarios de traducción
TIPOS_COMPROBANTES = {
    "1": "Factura",
    "2": "Liquidación_de_compra",
    "3": "Nota_de_crédito",
    "4": "Nota_de_débito",
    "6": "Comprobante_de_retención"
}

MESES = {
    "1": "Enero", "2": "Febrero", "3": "Marzo", "4": "Abril", "5": "Mayo", "6": "Junio",
    "7": "Julio", "8": "Agosto", "9": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}

def traducir_tipo(tipo_valor: str) -> str:
    return TIPOS_COMPROBANTES.get(tipo_valor, f"{tipo_valor}")

def traducir_mes(mes_valor: str) -> str:
    return MESES.get(mes_valor.lstrip("0"), f"{mes_valor}")

def obtener_ruta_descargas() -> Path:
    carpeta_descargas = Path(os.path.join(Path.home(), "Downloads"))
    if not carpeta_descargas.exists():
        carpeta_descargas = Path(os.path.join(Path.home(), "Descargas"))
        if not carpeta_descargas.exists():
            raise FileNotFoundError("🚨 No se encontró la carpeta de descargas predeterminada.")
    return carpeta_descargas

def descargar_comprobantes_txt(pagina: Page, tipo: str, mes: str, year: str):
    try:
        tipo_comprobante = traducir_tipo(tipo)
        mes = traducir_mes(mes)
        
        boton_descarga = pagina.locator("a#frmPrincipal\\:lnkTxtlistado")
    
        print("Iniciando descarga del comprobante...")
        with pagina.expect_download() as download_event:
            boton_descarga.click()
            
        descarga = download_event.value
        
        # Define la carpeta y el nombre del archivo
        carpeta_descargas = obtener_ruta_descargas()
        nombre_archivo = f"comprobante_{tipo_comprobante}_{mes}_{year}.txt"
        ruta_destino = carpeta_descargas / nombre_archivo
        
        # Guarda el archivo
        descarga.save_as(str(ruta_destino))
        print(f"Descarga completa ✅ Archivo: {ruta_destino}")
        
    except Exception as e:
        print(f"No se pudo descargar el comprobante\n{e}")

def descargar_xml(pagina: Page, tipo: str, mes: str, year: str):
    """
    Descarga múltiples archivos XML en la carpeta de descargas predeterminada,
    manejando la paginación correctamente y manteniendo los IDs secuenciales.
    """
    try:
        tipo_comprobante = traducir_tipo(tipo)
        mes = traducir_mes(mes)

        print("Iniciando descarga de los XML...")

        carpeta_descargas = obtener_ruta_descargas()
        contador_total = 0
        contador_global = 0  # ID general de comprobante que no se reinicia
        pagina_actual = 1

        while True:  # Bucle principal por página
            print(f"Procesando página {pagina_actual}...")
            i = 0  # Contador interno por página

            while True:  # Bucle interno por comprobante
                try:
                    selector = f"a#frmPrincipal\\:tablaCompRecibidos\\:{contador_global}\\:lnkXml"
                    boton_xml = pagina.locator(selector)

                    if not boton_xml.is_visible():
                        break

                    with pagina.expect_download() as download_event:
                        boton_xml.click()

                    descarga = download_event.value

                    nombre_xml = f"{tipo_comprobante}_{mes}_{year}_archivo_{contador_total + 1}.xml"
                    ruta_archivo = os.path.join(carpeta_descargas, nombre_xml)

                    descarga.save_as(ruta_archivo)
                    print(f"Archivo descargado: {ruta_archivo} ✅")

                    contador_total += 1
                    contador_global += 1
                    i += 1

                except Exception:
                    break  # Sale del bucle si hay error al acceder al comprobante

            # Si hay menos de 50 en esta página, ya no hay más comprobantes
            if i < 50:
                print(f"Se descargaron {contador_total} archivos en total. Finalizando.")
                break

            # Intentar pasar a la siguiente página
            try:
                boton_siguiente = pagina.locator("span.ui-paginator-next")
                if boton_siguiente.is_visible():
                    boton_siguiente.click()
                    print("Pasando a la siguiente página...")
                    pagina_actual += 1
                    pagina.wait_for_timeout(500)  # Espera breve para evitar errores de carga
                else:
                    print("No hay más páginas disponibles.")
                    break
            except Exception as e:
                print(f"Error al intentar pasar a la siguiente página: {e}")
                break

    except Exception as e:
        print(f"🚨 Error general durante la descarga de XML:\n{e}")