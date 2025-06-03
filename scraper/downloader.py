import os
import time
from playwright.sync_api import Page
from datetime import datetime

YEAR_ACTUAL = datetime.now().strftime("%Y")
MES_ACTUAL = datetime.now().strftime("%m")

MESES = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}

MES_NOMBRE = MESES.get(MES_ACTUAL, MES_ACTUAL)

CARPETA_DESCARGA_TXT = os.path.abspath("F:/a/proyectos/python/sri_scraper/downloads/comprobante_txt")

BASE_CARPETA_DESCARGA_XML = os.path.abspath("F:/a/proyectos/python/sri_scraper/downloads/archivos_xml")

CARPETAS_COMPROBANTES = {
    "1": os.path.join(BASE_CARPETA_DESCARGA_XML, "facturas"),
    "2": os.path.join(BASE_CARPETA_DESCARGA_XML, "liquidaciones"),
    "3": os.path.join(BASE_CARPETA_DESCARGA_XML, "credito"),
    "4": os.path.join(BASE_CARPETA_DESCARGA_XML, "debito"),
    "6": os.path.join(BASE_CARPETA_DESCARGA_XML, "retenciones"),
}

TIPOS_COMPROBANTES = {
    "1": "Factura",
    "2": "Liquidación",
    "3": "Nota_de_crédito",
    # "4": "Nota_de_débito",
    "6": "Comprobante_de_retención"
}

def traducir_tipo(tipo_valor: str) -> str:
    return TIPOS_COMPROBANTES.get(tipo_valor, tipo_valor)

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

        # Intento con UTF-8 primero, si falla probamos con Latin-1
        try:
            # Leer el contenido primero con UTF-8
            contenido = descarga.path().read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Si falla UTF-8, intentar con ISO-8859-1 (Latin-1)
            try:
                contenido = descarga.path().read_text(encoding='iso-8859-1')
                # Convertir a UTF-8
                contenido = contenido.encode('utf-8', errors='replace').decode('utf-8')
            except Exception as e:
                print(f"⚠️ No se pudo decodificar el archivo: {e}")
                # Último recurso: guardar tal cual
                descarga.save_as(ruta_destino)
                print(f"Archivo guardado en formato original en {ruta_destino}")
                return

        # Guardar el contenido en UTF-8
        with open(ruta_destino, 'w', encoding='utf-8') as f:
            f.write(contenido)

        print(f"Archivo guardado correctamente en UTF-8 en {ruta_destino}")
        print("Descarga de TXT completada ✅")

    except Exception as e:
        print(f"🚨 Error durante la descarga del comprobante TXT: {str(e)}")

def descargar_xml(pagina: Page, tipo: str):
    try:
        tipo_comprobante = traducir_tipo(tipo)
        carpeta_descargas = CARPETAS_COMPROBANTES.get(tipo, BASE_CARPETA_DESCARGA_XML)
        contador_total = 0
        pagina_actual = 1
        indice_inicial = 0  # Mantener un índice global para los IDs de elementos

        print("Iniciando descarga de los XML...")

        while True:
            print(f"Procesando página {pagina_actual}...")
            descargas_en_pagina = 0
            i = indice_inicial  # Usar el índice global como punto de partida

            while True:
                try:
                    selector = f"a#frmPrincipal\\:tablaCompRecibidos\\:{i}\\:lnkXml"
                    boton_xml = pagina.locator(selector)

                    if not boton_xml.is_visible(timeout=100):  # Añadir timeout explícito
                        break

                    with pagina.expect_download() as download_event:
                        boton_xml.click()
                        pagina.wait_for_timeout(100)  # Pequeña pausa para evitar sobrecarga

                    descarga = download_event.value

                    nombre_xml = f"{tipo_comprobante}_{MES_NOMBRE}_{YEAR_ACTUAL}_archivo_{contador_total + 1}.xml"
                    ruta_archivo = os.path.join(carpeta_descargas, nombre_xml)

                    descarga.save_as(ruta_archivo)
                    print(f"Archivo descargado: {ruta_archivo} ✅")

                    contador_total += 1
                    descargas_en_pagina += 1
                    i += 1

                except Exception as e:
                    print(f"Error en descarga individual (ID {i}): {str(e)}")
                    break

            # Actualizar el índice inicial para la próxima página
            indice_inicial = i

            # Verificar si debemos continuar con la siguiente página
            boton_siguiente = pagina.locator("span.ui-paginator-next")
            
            if descargas_en_pagina >= 50 and boton_siguiente.is_visible() and not "ui-state-disabled" in boton_siguiente.get_attribute("class"):
                try:
                    boton_siguiente.click()
                    print("Pasando a la siguiente página...")
                    pagina_actual += 1
                    pagina.wait_for_selector(f"a#frmPrincipal\\:tablaCompRecibidos\\:{indice_inicial}\\:lnkXml", timeout=5000)  # Esperar carga
                except Exception as e:
                    print(f"Error al intentar pasar a la siguiente página: {e}")
                    break
            else:
                print(f"Se descargaron {contador_total} archivos en total. Finalizando.")
                break

    except Exception as e:
        print(f"🚨 Error general durante la descarga de XML:\n{e}")


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
        
        pagina.wait_for_timeout(1000)
        
        tabla_comprobantes = pagina.locator("div#frmPrincipal\:tablaCompRecibidos")
        if tabla_comprobantes.count() == 0:
            print(f"⚠️ No existen comprobantes para {traducir_tipo(tipo)}. Saltando al siguiente tipo...")
            return

        print("Descargando comprobante TXT...")
        descargar_comprobantes_txt(pagina, tipo)

        print("Descargando comprobantes XML...")
        descargar_xml(pagina, tipo)
        
        # Recargar la página para evitar el bug del SRI
        print("\nRecargando página para limpiar estado...")
        pagina.reload()
        pagina.wait_for_load_state("networkidle")
        pagina.wait_for_timeout(3000)  # Espera generosa después de recargar

        print(f"\n✅ Proceso completado para {traducir_tipo(tipo)}")

    except Exception as e:
        print(f"Error procesando el comprobante {traducir_tipo(tipo)} (value: {tipo}): {e}")
        try:
            pagina.reload()
            pagina.wait_for_load_state("networkidle")
        except:
            pass
        raise


def automatizar_y_descargar(pagina: Page):
    print("\nIniciando el proceso automático de consulta y descarga de comprobantes...")

    for tipo, nombre in TIPOS_COMPROBANTES.items():
        print(f"\nProcesando comprobantes para: {nombre} (value: {tipo})")
        procesar_tipo_comprobante(pagina, tipo)

    print("\nProceso automático completado.")