import pandas as pd
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import logging

# Configuración de rutas
BASE_DIR = "F:/a/proyectos/python/sri_scraper/downloads"
CARPETA_XML_NOTAS_CREDITO = os.path.join(BASE_DIR, "archivos_xml", "credito")
CARPETA_TXT = os.path.join(BASE_DIR, "comprobante_txt")
CARPETA_DETALLES_NC = os.path.join(BASE_DIR, "detalles_notas_credito")

def configurar_carpetas():
    """Asegura que las carpetas existan"""
    os.makedirs(CARPETA_XML_NOTAS_CREDITO, exist_ok=True)
    os.makedirs(CARPETA_TXT, exist_ok=True)
    os.makedirs(CARPETA_DETALLES_NC, exist_ok=True)

def extraer_detalles_nota_credito(comprobante_root, clave_acceso):
    """Extrae los detalles de una nota de crédito y devuelve lista de diccionarios"""
    detalles = []
    
    try:
        # Información básica del comprobante
        info_tributaria = comprobante_root.find(".//infoTributaria")
        info_nota_credito = comprobante_root.find(".//infoNotaCredito")
        
        if info_tributaria is None or info_nota_credito is None:
            logging.warning("Estructura XML no es una nota de crédito válida")
            return detalles
        
        datos_base = {
            "CLAVE_ACCESO": clave_acceso,
            "RUC_EMISOR": info_tributaria.findtext("ruc", "").strip(),
            "RAZON_SOCIAL_EMISOR": info_tributaria.findtext("razonSocial", "").strip(),
            "FECHA_EMISION": info_nota_credito.findtext("fechaEmision", "").strip()
        }

        # Procesar cada detalle de producto
        for detalle in comprobante_root.findall(".//detalle"):
            try:
                detalle_data = datos_base.copy()
                detalle_data.update({
                    "DESCRIPCION": detalle.findtext("descripcion", "").strip(),
                    "CANTIDAD": detalle.findtext("cantidad", "0").strip(),
                    "PRECIO_UNITARIO": detalle.findtext("precioUnitario", "0.00").strip(),
                    "DESCUENTO": detalle.findtext("descuento", "0.00").strip(),
                    "PRECIO_TOTAL_SIN_IMPUESTO": detalle.findtext("precioTotalSinImpuesto", "0.00").strip()
                })

                # Procesar impuestos del detalle (solo IVA)
                impuestos = detalle.find(".//impuestos")
                if impuestos is not None:
                    for impuesto in impuestos.findall(".//impuesto"):
                        if impuesto.findtext("codigo", "") == "2":  # IVA
                            detalle_data.update({
                                "TARIFA_IVA": impuesto.findtext("tarifa", "0").strip(),
                                "VALOR_IVA": impuesto.findtext("valor", "0.00").strip()
                            })

                detalles.append(detalle_data)
            except Exception as e:
                logging.warning(f"Error procesando detalle: {str(e)}")
                continue
        
        return detalles
    
    except Exception as e:
        logging.error(f"Error en extraer_detalles_nota_credito: {str(e)}")
        return []

def procesar_xml_nota_credito(xml_path):
    """Procesa un XML de nota de crédito y devuelve los detalles"""
    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Verificar si es un XML de autorización que contiene una nota de crédito
            if 'notaCredito' not in contenido:
                logging.warning(f"El archivo {os.path.basename(xml_path)} no es una nota de crédito")
                return []
            
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            comprobante = root.find(".//comprobante")
            if comprobante is None:
                logging.warning(f"No se encontró el elemento comprobante en {os.path.basename(xml_path)}")
                return []
            
            try:
                comprobante_root = ET.fromstring(comprobante.text.strip())
            except ET.ParseError:
                logging.error(f"Error al parsear el contenido XML en {os.path.basename(xml_path)}")
                return []
            
            clave_acceso = comprobante_root.findtext(".//claveAcceso", default="").strip()
            if not clave_acceso:
                logging.warning(f"Clave de acceso no encontrada en {os.path.basename(xml_path)}")
                return []
            
            detalles = extraer_detalles_nota_credito(comprobante_root, clave_acceso)
            return detalles

    except Exception as e:
        logging.error(f"Error al procesar el XML {os.path.basename(xml_path)}: {str(e)}")
        return []

def generar_archivo_detalles_notas_credito():
    """Función principal para generar el archivo de detalles de notas de crédito"""
    try:
        configurar_carpetas()
        
        logging.info(f"Buscando archivos XML en: {CARPETA_XML_NOTAS_CREDITO}")
        
        # Verificar si la carpeta existe y tiene archivos
        if not os.path.exists(CARPETA_XML_NOTAS_CREDITO):
            logging.error(f"La carpeta {CARPETA_XML_NOTAS_CREDITO} no existe")
            return None
        
        archivos = [f for f in os.listdir(CARPETA_XML_NOTAS_CREDITO) if f.lower().endswith('.xml')]
        
        if not archivos:
            logging.warning(f"No se encontraron archivos XML en {CARPETA_XML_NOTAS_CREDITO}")
            return None
        
        logging.info(f"Se encontraron {len(archivos)} archivos XML para procesar")
        
        # Lista para acumular todos los detalles
        todos_detalles = []
        xml_procesados = 0
        detalles_procesados = 0
        
        for archivo in archivos:
            xml_path = os.path.join(CARPETA_XML_NOTAS_CREDITO, archivo)
            try:
                detalles = procesar_xml_nota_credito(xml_path)
                if detalles:
                    todos_detalles.extend(detalles)
                    detalles_procesados += len(detalles)
                    xml_procesados += 1
                    logging.info(f"Procesado: {archivo} - {len(detalles)} detalles")
            except Exception as e:
                logging.error(f"Error procesando {archivo}: {str(e)}")
                continue
        
        # Crear DataFrame con todos los detalles
        if not todos_detalles:
            logging.warning("No se encontraron detalles válidos de notas de crédito en los XML")
            return None
        
        df_detalles = pd.DataFrame(todos_detalles)
        
        # Ordenar columnas
        column_order = [
            'CLAVE_ACCESO', 'RUC_EMISOR', 'RAZON_SOCIAL_EMISOR', 'FECHA_EMISION',
            'DESCRIPCION', 'CANTIDAD', 'PRECIO_UNITARIO',
            'DESCUENTO', 'PRECIO_TOTAL_SIN_IMPUESTO', 'TARIFA_IVA', 'VALOR_IVA'
        ]
        
        # Filtrar solo las columnas que existen en los datos
        column_order = [col for col in column_order if col in df_detalles.columns]
        df_detalles = df_detalles[column_order]
        
        # Generar nombre de archivo con fecha
        mes_actual = datetime.now().strftime("%m")
        año_actual = datetime.now().strftime("%Y")
        nombre_archivo = f"detalles_notas_credito_{mes_actual}_{año_actual}.txt"
        ruta_salida = os.path.join(CARPETA_DETALLES_NC, nombre_archivo)
        
        # Guardar el archivo
        df_detalles.to_csv(ruta_salida, sep="\t", index=False, encoding="utf-8")
        
        # Resumen de ejecución
        print("\n" + "="*50)
        print("RESUMEN DE EJECUCIÓN")
        print(f"- Carpeta XML escaneada: {CARPETA_XML_NOTAS_CREDITO}")
        print(f"- Archivos XML encontrados: {len(archivos)}")
        print(f"- XMLs procesados correctamente: {xml_procesados}")
        print(f"- Detalles encontrados: {detalles_procesados}")
        print(f"- Archivo generado: {ruta_salida}")
        print("="*50)
        
        return ruta_salida
    
    except Exception as e:
        logging.error(f"ERROR CRÍTICO: {str(e)}", exc_info=True)
        raise