import pandas as pd
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import logging

# Configuración de rutas
BASE_DIR = "F:/a/proyectos/python/sri_scraper/downloads"
CARPETA_XML_RETENCIONES = os.path.join(BASE_DIR, "archivos_xml/retenciones")
CARPETA_TXT = os.path.join(BASE_DIR, "comprobante_txt")
CARPETA_DETALLES_RETENCIONES = os.path.join(BASE_DIR, "detalles_retenciones")

def configurar_carpetas():
    """Asegura que las carpetas existan"""
    os.makedirs(CARPETA_XML_RETENCIONES, exist_ok=True)
    os.makedirs(CARPETA_TXT, exist_ok=True)
    os.makedirs(CARPETA_DETALLES_RETENCIONES, exist_ok=True)

def extraer_detalles_retencion(comprobante_root, clave_acceso):
    """Extrae los detalles de retención de un XML y devuelve lista de diccionarios"""
    detalles = []
    
    try:
        # Información básica del comprobante
        info_tributaria = comprobante_root.find(".//infoTributaria")
        info_comp_retencion = comprobante_root.find(".//infoCompRetencion")
        
        if info_tributaria is None or info_comp_retencion is None:
            raise ValueError("Estructura XML incompleta - faltan secciones infoTributaria o infoCompRetencion")
        
        datos_base = {
            "CLAVE_ACCESO": clave_acceso,
            "RUC_EMISOR": info_tributaria.findtext("ruc", "").strip(),
            "RAZON_SOCIAL_EMISOR": info_tributaria.findtext("razonSocial", "").strip(),
            "NOMBRE_COMERCIAL": info_tributaria.findtext("nombreComercial", "").strip(),
            "COD_DOC": info_tributaria.findtext("codDoc", "").strip(),
            "ESTAB": info_tributaria.findtext("estab", "").strip(),
            "PTO_EMI": info_tributaria.findtext("ptoEmi", "").strip(),
            "SECUENCIAL": info_tributaria.findtext("secuencial", "").strip(),
            "DIR_MATRIZ": info_tributaria.findtext("dirMatriz", "").strip(),
            "FECHA_EMISION": info_comp_retencion.findtext("fechaEmision", "").strip(),
            "DIR_ESTABLECIMIENTO": info_comp_retencion.findtext("dirEstablecimiento", "").strip(),
            "CONTRIBUYENTE_ESPECIAL": info_comp_retencion.findtext("contribuyenteEspecial", "").strip(),
            "OBLIGADO_CONTABILIDAD": info_comp_retencion.findtext("obligadoContabilidad", "").strip(),
            "TIPO_IDENTIFICACION_SUJETO": info_comp_retencion.findtext("tipoIdentificacionSujetoRetenido", "").strip(),
            "RAZON_SOCIAL_SUJETO": info_comp_retencion.findtext("razonSocialSujetoRetenido", "").strip(),
            "IDENTIFICACION_SUJETO": info_comp_retencion.findtext("identificacionSujetoRetenido", "").strip(),
            "PERIODO_FISCAL": info_comp_retencion.findtext("periodoFiscal", "").strip()
        }

        # Procesar cada impuesto/retención
        impuestos = comprobante_root.find(".//impuestos")
        if impuestos is not None:
            for impuesto in impuestos.findall(".//impuesto"):
                try:
                    detalle = datos_base.copy()
                    detalle.update({
                        "CODIGO": impuesto.findtext("codigo", "").strip(),
                        "CODIGO_RETENCION": impuesto.findtext("codigoRetencion", "").strip(),
                        "BASE_IMPONIBLE": impuesto.findtext("baseImponible", "0.00").strip(),
                        "PORCENTAJE_RETENCION": impuesto.findtext("porcentajeRetener", "0.00").strip(),
                        "VALOR_RETENIDO": impuesto.findtext("valorRetenido", "0.00").strip(),
                        "COD_DOC_SUSTENTO": impuesto.findtext("codDocSustento", "").strip(),
                        "NUM_DOC_SUSTENTO": impuesto.findtext("numDocSustento", "").strip(),
                        "FECHA_EMISION_DOC_SUSTENTO": impuesto.findtext("fechaEmisionDocSustento", "").strip()
                    })
                    detalles.append(detalle)
                except Exception as e:
                    logging.warning(f"Error procesando impuesto: {str(e)}")
                    continue
        
        return detalles
    
    except Exception as e:
        logging.error(f"Error en extraer_detalles_retencion: {str(e)}")
        return []

def procesar_xml_retencion(xml_path):
    """Procesa un XML de retención y devuelve los detalles"""
    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            comprobante = root.find(".//comprobante")
            if comprobante is None:
                raise ValueError("No se encontró el elemento comprobante en el XML")
            
            comprobante_root = ET.fromstring(comprobante.text.strip())
            
            clave_acceso = comprobante_root.findtext(".//claveAcceso", default="").strip()
            if not clave_acceso:
                raise ValueError("Clave de acceso no encontrada o vacía")
            
            detalles = extraer_detalles_retencion(comprobante_root, clave_acceso)
            return detalles

    except Exception as e:
        logging.error(f"Error al procesar el XML {xml_path}: {str(e)}")
        return []

def generar_archivo_detalles_retenciones():
    """Función principal para generar el archivo de detalles de retenciones"""
    try:
        configurar_carpetas()
        
        logging.info("Iniciando procesamiento de detalles de retenciones...")
        
        # Lista para acumular todos los detalles
        todos_detalles = []
        
        # Procesar todos los XML en la carpeta
        xml_procesados = 0
        retenciones_procesadas = 0
        
        for archivo in os.listdir(CARPETA_XML_RETENCIONES):
            if archivo.lower().endswith(".xml"):
                xml_path = os.path.join(CARPETA_XML_RETENCIONES, archivo)
                try:
                    detalles = procesar_xml_retencion(xml_path)
                    if detalles:
                        todos_detalles.extend(detalles)
                        retenciones_procesadas += len(detalles)
                        xml_procesados += 1
                        logging.info(f"Procesado: {archivo} - {len(detalles)} retenciones")
                except Exception as e:
                    logging.error(f"Error procesando {archivo}: {str(e)}")
                    continue
        
        # Crear DataFrame con todos los detalles
        if not todos_detalles:
            logging.warning("No se encontraron detalles de retenciones en los XML")
            return
        
        df_detalles = pd.DataFrame(todos_detalles)
        
        # Ordenar columnas
        column_order = [
            'CLAVE_ACCESO', 'RUC_EMISOR', 'RAZON_SOCIAL_EMISOR', 
            'NOMBRE_COMERCIAL', 'FECHA_EMISION', 'CODIGO_RETENCION',
            'BASE_IMPONIBLE', 'PORCENTAJE_RETENCION', 'VALOR_RETENIDO'
        ]
        
        # Filtrar solo las columnas que existen en los datos
        column_order = [col for col in column_order if col in df_detalles.columns]
        df_detalles = df_detalles[column_order]
        
        # Generar nombre de archivo con fecha
        mes_actual = datetime.now().strftime("%m")
        año_actual = datetime.now().strftime("%Y")
        nombre_archivo = f"detalles_retenciones_{mes_actual}_{año_actual}.txt"
        ruta_salida = os.path.join(CARPETA_DETALLES_RETENCIONES, nombre_archivo)
        
        # Guardar el archivo
        df_detalles.to_csv(ruta_salida, sep="\t", index=False, encoding="utf-8")
        
        # Resumen de ejecución
        print("\n" + "="*50)
        print("RESUMEN DE EJECUCIÓN")
        print(f"- XMLs procesados: {xml_procesados}")
        print(f"- Retenciones encontradas: {retenciones_procesadas}")
        print(f"- Archivo generado: {ruta_salida}")
        print("="*50)
        
        return ruta_salida
    
    except Exception as e:
        logging.error(f"ERROR CRÍTICO: {str(e)}", exc_info=True)
        raise