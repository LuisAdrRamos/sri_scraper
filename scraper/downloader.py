import os
import time
from playwright.sync_api import Page
from datetime import datetime

# ------------------ Configuración Global ------------------
YEAR_ACTUAL = datetime.now().strftime("%Y")
MES_ACTUAL = datetime.now().strftime("%m")
MESES = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}
MES_NOMBRE = MESES.get(MES_ACTUAL, MES_ACTUAL)

CARPETA_DESCARGA_TXT = os.path.abspath("F:/a/proyectos/python/sri_scraper/downloads/comprobante_txt")
CARPETA_DESCARGA_XML = os.path.abspath("F:/a/proyectos/python/sri_scraper/downloads/archivos_xml")

# Tipos de comprobantes solicitados: "1" (Factura) y "6" (Comprobante de Retención)
TIPOS_COMPROBANTES = {
    "1": "Factura",
    "6": "Comprobante_de_retención"
}

# ------------------ Funciones de Ayuda ------------------
def traducir_tipo(tipo_valor: str) -> str:
    return TIPOS_COMPROBANTES.get(tipo_valor, tipo_valor)

# ------------------ Funciones de Descarga ------------------
def descargar_comprobantes_txt(pagina: Page, tipo: str):
    try:
        tipo_comprobante = traducir_tipo(tipo)
        boton_descarga = pagina.locator("a#frmPrincipal\\:lnkTxtlistado")

        print("Iniciando descarga del comprobante TXT...")
        with pagina.expect_download() as download_event:
            boton_descarga.click()

        descarga = download_event.value
        nombre_archivo = f"comprobante_{tipo_comprobante}_{MES_NOMBRE}_{YEAR_ACTUAL}.txt"
        ruta_destino = os.path.join(CARPETA_DESCARGA_TXT, nombre_archivo)

        descarga.save_as(ruta_destino)
        print(f"Archivo guardado en {ruta_destino}")
        print("Descarga de TXT completada ✅")

    except Exception as e:
        print(f"🚨 Error durante la descarga del comprobante TXT: {e}")

def descargar_xml(pagina: Page, tipo: str):
    try:
        tipo_comprobante = traducir_tipo(tipo)
        i = 0
        # tiempo_inicio = time.time()
        # tiempo_limite = 10  # Máximo tiempo de espera en segundos

        print("Iniciando descarga de los XML...")

        while True:
            try:
                # Verificar si el tiempo excede el límite
                # if time.time() - tiempo_inicio > tiempo_limite:
                #     print(f"⏳ Tiempo límite alcanzado ({tiempo_limite} seg). Finalizando descarga de XML.")
                #     break

                selector = f"a#frmPrincipal\\:tablaCompRecibidos\\:{i}\\:lnkXml"
                boton_xml = pagina.locator(selector)

                with pagina.expect_download() as download_event:
                    boton_xml.click()

                descarga = download_event.value
                nombre_xml = f"{tipo_comprobante}_{i+1}_{MES_NOMBRE}_{YEAR_ACTUAL}.xml"
                ruta_archivo = os.path.join(CARPETA_DESCARGA_XML, nombre_xml)
                descarga.save_as(ruta_archivo)

                print(f"Descargado archivo {nombre_xml}")
                i += 1

            except Exception:
                print(f"Se encontraron {i} archivos XML. Finalizando descarga.")
                break

    except Exception as e:
        print(f"🚨 Error general durante la descarga de XML:\n{e}")

# ------------------ Automatización de Consulta y Descarga ------------------
def procesar_tipo_comprobante(pagina: Page, tipo: str):
    try:
        print("Seleccionando todos los días (valor '0')...")
        pagina.select_option("select#frmPrincipal\\:dia", "0")

        print("Activando el menú desplegable de tipo de comprobante...")
        pagina.click("select#frmPrincipal\\:cmbTipoComprobante")
        print(f"Seleccionando comprobante con value: {tipo}...")
        pagina.select_option("select#frmPrincipal\\:cmbTipoComprobante", tipo)

        print("Ejecutando la consulta...")
        pagina.click("button#frmPrincipal\\:btnConsultar")
        pagina.wait_for_load_state("networkidle")

        print("Descargando comprobante TXT...")
        descargar_comprobantes_txt(pagina, tipo)

        print("Descargando comprobantes XML...")
        descargar_xml(pagina, tipo)

    except Exception as e:
        print(f"Error procesando el comprobante {traducir_tipo(tipo)} (value: {tipo}): {e}")

def automatizar_y_descargar(pagina: Page):
    print("\nIniciando el proceso automático de consulta y descarga de comprobantes...")

    for tipo, nombre in TIPOS_COMPROBANTES.items():
        print(f"\nProcesando comprobantes para: {nombre} (value: {tipo})")
        procesar_tipo_comprobante(pagina, tipo)

    print("\nProceso automático completado.")