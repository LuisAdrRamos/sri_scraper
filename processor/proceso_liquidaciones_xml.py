import pandas as pd
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import logging

# Configuración de rutas
BASE_DIR = "F:/a/proyectos/python/sri_scraper/downloads"
CARPETA_XML_LIQUIDACIONES = os.path.join(BASE_DIR, "archivos_xml/liquidaciones")
CARPETA_TXT = os.path.join(BASE_DIR, "comprobante_txt")
CARPETA_DETALLES_LIQUIDACIONES = os.path.join(BASE_DIR, "detalles_liquidaciones")

def configurar_carpetas():
    """Asegura que las carpetas existan"""
    try:
        os.makedirs(CARPETA_XML_LIQUIDACIONES, exist_ok=True)
        os.makedirs(CARPETA_TXT, exist_ok=True)
        os.makedirs(CARPETA_DETALLES_LIQUIDACIONES, exist_ok=True)
    except Exception as e:
        logging.error(f"Error al crear carpetas: {str(e)}")
        raise

def procesar_xml_liquidacion(xml_path):
    """Procesa un XML de liquidación y devuelve un diccionario con los datos"""
    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            # Obtener el elemento comprobante
            comprobante = root.find(".//comprobante")
            if comprobante is None:
                raise ValueError("No se encontró el elemento comprobante en el XML")
            
            comprobante_root = ET.fromstring(comprobante.text.strip())
            
            # Extraer información básica
            clave_acceso = comprobante_root.findtext(".//claveAcceso", "").strip()
            if not clave_acceso:
                raise ValueError("Clave de acceso no encontrada o vacía")
            
            info_tributaria = comprobante_root.find(".//infoTributaria")
            if info_tributaria is None:
                raise ValueError("No se encontró infoTributaria en el XML")
            
            ruc = info_tributaria.findtext("ruc", "").strip()
            razon_social = info_tributaria.findtext("razonSocial", "").strip()
            
            # Extraer información de proveedor/comprador
            razon_social_proveedor = comprobante_root.findtext(".//razonSocialProveedor", "").strip()
            if not razon_social_proveedor:
                razon_social_proveedor = comprobante_root.findtext(".//razonSocialComprador", "").strip()
            
            identificacion_proveedor = comprobante_root.findtext(".//identificacionProveedor", "").strip()
            if not identificacion_proveedor:
                identificacion_proveedor = comprobante_root.findtext(".//identificacionComprador", "").strip()
            
            fecha_emision = comprobante_root.findtext(".//fechaEmision", "").strip()
            
            # Extraer información de impuestos
            impuestos = []
            total_con_impuestos = comprobante_root.find(".//totalConImpuestos")
            if total_con_impuestos is not None:
                for impuesto in total_con_impuestos.findall(".//totalImpuesto"):
                    impuesto_data = {
                        "descuento_adicional": impuesto.findtext("descuentoAdicional", "0.00").strip(),
                        "base_imponible": impuesto.findtext("baseImponible", "0.00").strip(),
                        "tarifa": impuesto.findtext("tarifa", "0").strip(),
                        "valor": impuesto.findtext("valor", "0.00").strip()
                    }
                    impuestos.append(impuesto_data)
            
            importe_total = comprobante_root.findtext(".//importeTotal", "0.00").strip()
            
            # Construir el diccionario con los datos
            liquidacion = {
                "CLAVE_ACCESO": clave_acceso,
                "RUC": ruc,
                "RAZON_SOCIAL": razon_social,
                "FECHA_EMISION": fecha_emision,
                "RAZON_SOCIAL_PROVEEDOR": razon_social_proveedor,
                "IDENTIFICACION_PROVEEDOR": identificacion_proveedor,
                "IMPORTE_TOTAL": importe_total,
                "IMPUESTOS": impuestos
            }
            
            return liquidacion
    
    except ET.ParseError as e:
        logging.error(f"Error al parsear el XML {xml_path}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Error al procesar el XML {xml_path}: {str(e)}")
        return None

def generar_archivo_detalles_liquidaciones():
    """Función principal para generar el archivo de detalles de liquidaciones"""
    try:
        configurar_carpetas()
        
        # Verificar si hay archivos XML en la carpeta
        if not os.listdir(CARPETA_XML_LIQUIDACIONES):
            logging.warning(f"No se encontraron archivos XML en {CARPETA_XML_LIQUIDACIONES}")
            return None
        
        logging.info("Iniciando procesamiento de liquidaciones...")
        
        # Lista para acumular todos los detalles
        todas_liquidaciones = []
        
        # Procesar todos los XML en la carpeta
        xml_procesados = 0
        xml_con_error = 0
        
        for archivo in os.listdir(CARPETA_XML_LIQUIDACIONES):
            if archivo.lower().endswith(".xml"):
                xml_path = os.path.join(CARPETA_XML_LIQUIDACIONES, archivo)
                try:
                    liquidacion = procesar_xml_liquidacion(xml_path)
                    if liquidacion:
                        # Aplanar la información de impuestos
                        if liquidacion["IMPUESTOS"]:
                            for impuesto in liquidacion["IMPUESTOS"]:
                                liquidacion_plana = {
                                    "CLAVE_ACCESO": liquidacion["CLAVE_ACCESO"],
                                    "RUC": liquidacion["RUC"],
                                    "RAZON_SOCIAL": liquidacion["RAZON_SOCIAL"],
                                    "FECHA_EMISION": liquidacion["FECHA_EMISION"],
                                    "RAZON_SOCIAL_PROVEEDOR": liquidacion["RAZON_SOCIAL_PROVEEDOR"],
                                    "IDENTIFICACION_PROVEEDOR": liquidacion["IDENTIFICACION_PROVEEDOR"],
                                    "DESCUENTO_ADICIONAL": impuesto["descuento_adicional"],
                                    "BASE_IMPONIBLE": impuesto["base_imponible"],
                                    "TARIFA": impuesto["tarifa"],
                                    "VALOR_IMPUESTO": impuesto["valor"],
                                    "IMPORTE_TOTAL": liquidacion["IMPORTE_TOTAL"]
                                }
                                todas_liquidaciones.append(liquidacion_plana)
                        else:
                            # Si no hay impuestos, añadir igual el registro
                            liquidacion_plana = {
                                "CLAVE_ACCESO": liquidacion["CLAVE_ACCESO"],
                                "RUC": liquidacion["RUC"],
                                "RAZON_SOCIAL": liquidacion["RAZON_SOCIAL"],
                                "FECHA_EMISION": liquidacion["FECHA_EMISION"],
                                "RAZON_SOCIAL_PROVEEDOR": liquidacion["RAZON_SOCIAL_PROVEEDOR"],
                                "IDENTIFICACION_PROVEEDOR": liquidacion["IDENTIFICACION_PROVEEDOR"],
                                "DESCUENTO_ADICIONAL": "0.00",
                                "BASE_IMPONIBLE": "0.00",
                                "TARIFA": "0",
                                "VALOR_IMPUESTO": "0.00",
                                "IMPORTE_TOTAL": liquidacion["IMPORTE_TOTAL"]
                            }
                            todas_liquidaciones.append(liquidacion_plana)
                        
                        xml_procesados += 1
                    else:
                        xml_con_error += 1
                except Exception as e:
                    logging.error(f"Error procesando {archivo}: {str(e)}")
                    xml_con_error += 1
                    continue
        
        # Crear DataFrame con todos los detalles
        if not todas_liquidaciones:
            logging.warning("No se encontraron liquidaciones válidas en los XML")
            return None
        
        df_liquidaciones = pd.DataFrame(todas_liquidaciones)
        
        # Ordenar columnas
        column_order = [
            'CLAVE_ACCESO', 'RUC', 'RAZON_SOCIAL', 'FECHA_EMISION',
            'RAZON_SOCIAL_PROVEEDOR', 'IDENTIFICACION_PROVEEDOR',
            'DESCUENTO_ADICIONAL', 'BASE_IMPONIBLE', 'TARIFA',
            'VALOR_IMPUESTO', 'IMPORTE_TOTAL'
        ]
        df_liquidaciones = df_liquidaciones[column_order]
        
        # Generar nombre de archivo con fecha
        mes_actual = datetime.now().strftime("%m")
        año_actual = datetime.now().strftime("%Y")
        nombre_archivo = f"detalles_liquidaciones_{mes_actual}_{año_actual}.txt"
        ruta_salida = os.path.join(CARPETA_DETALLES_LIQUIDACIONES, nombre_archivo)
        
        # Guardar el archivo
        df_liquidaciones.to_csv(ruta_salida, sep="\t", index=False, encoding="utf-8")
        
        # Resumen de ejecución
        print("\n" + "="*50)
        print("RESUMEN DE EJECUCIÓN")
        print(f"- XMLs procesados correctamente: {xml_procesados}")
        print(f"- XMLs con errores: {xml_con_error}")
        print(f"- Registros generados: {len(df_liquidaciones)}")
        print(f"- Archivo generado: {ruta_salida}")
        print("="*50)
        
        return ruta_salida
    
    except Exception as e:
        logging.error(f"ERROR CRÍTICO: {str(e)}", exc_info=True)
        raise

generar_archivo_detalles_liquidaciones()