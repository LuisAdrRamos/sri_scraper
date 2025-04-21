import os 
from playwright.sync_api import Page

CARPETA_DESCARGA_TXT = os.path.abspath("F:/a/proyectos/python/sri_scraper/downloads/comprobante_txt")
CARPETA_DESCARGA_XML = os.path.abspath("F:/a/proyectos/python/sri_scraper/downloads/archivos_xml")

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

def descargar_comprobantes_txt(pagina: Page, tipo: str, mes: str, year: str):
    try:
        tipo_comprobante = traducir_tipo(tipo)
        
        mes = traducir_mes(mes)
        
        boton_descarga = pagina.locator("a#frmPrincipal\\:lnkTxtlistado")
    
        print("Iniciando descarga del comprobante")
        with pagina.expect_download() as download_event:
            boton_descarga.click()
            
        descarga = download_event.value
        
        nombre_archivo = f"comprobante_{tipo_comprobante}_{mes}_{year}.txt"
        ruta_destino = os.path.join(CARPETA_DESCARGA_TXT, nombre_archivo)
        
        print(f"Archivo guardado en {ruta_destino}")
        descarga.save_as(ruta_destino)
        
        print("Descarga Completa ✅")
        
    except Exception as e:
        print(f"No se pudo descargar el comprobante\n{e}")
        

def descargar_xml(pagina: Page, tipo: str, mes: str, year: str):
    try:
        tipo_comprobante = traducir_tipo(tipo)
        mes = traducir_mes(mes)
        
        print("Iniciando descarga de los XML...")
        
        i = 0
        while True:
            try:
                selector = f"a#frmPrincipal\\:tablaCompRecibidos\\:{i}\\:lnkXml"
                boton_xml = pagina.locator(selector)
                
                with pagina.expect_download() as download_event:
                    boton_xml.click()
                
                descarga = download_event.value
                nombre_xml = f"{tipo_comprobante}{i+1}_{mes}_{year}.xml"
                ruta_archivo = os.path.join(CARPETA_DESCARGA_XML, nombre_xml)
                descarga.save_as(ruta_archivo)
                
                print(f"Descargado archivo {nombre_xml}")
                i += 1
                
            except Exception:
                print(f"Se encontraron {i} archivos .xml, Finalizando descarga.")
                
                break
        
    except Exception as e:
        print(f"🚨 Error general durante la descarga de XML:\n{e}")