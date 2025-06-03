import pandas as pd
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import logging

# Configuración de rutas
BASE_DIR = "F:/a/proyectos/python/sri_scraper/downloads"
CARPETA_XML_FACTURAS = os.path.join(BASE_DIR, "archivos_xml/facturas")
CARPETA_TXT = os.path.join(BASE_DIR, "comprobante_txt")
CARPETA_DETALLES = os.path.join(BASE_DIR, "detalles_productos")

def configurar_carpetas():
    """Asegura que las carpetas existan"""
    os.makedirs(CARPETA_XML_FACTURAS, exist_ok=True)
    os.makedirs(CARPETA_TXT, exist_ok=True)
    os.makedirs(CARPETA_DETALLES, exist_ok=True)

def extraer_detalles_productos(comprobante_root, clave_acceso):
    """Extrae los detalles de productos de un XML de factura y devuelve lista de diccionarios"""
    detalles = []
    
    try:
        # Obtener información tributaria del emisor
        info_tributaria = comprobante_root.find(".//infoTributaria")
        
        info_factura = comprobante_root.find(".//infoFactura")
        
        ruc_emisor = info_tributaria.findtext("ruc", "").strip()
        razon_social = info_tributaria.findtext("razonSocial", "").strip()
        fecha_emision = info_factura.findtext("fechaEmision", "").strip()
        
        for detalle in comprobante_root.findall(".//detalle"):
            try:
                producto = {
                    "CLAVE_ACCESO": clave_acceso,
                    "RUC_EMISOR": ruc_emisor,
                    "RAZON_SOCIAL_EMISOR": razon_social,
                    "FECHA_EMISION": fecha_emision,
                    "Producto": detalle.findtext("descripcion", default="").strip(),
                    "Código": detalle.findtext("codigoPrincipal", default="").strip(),
                    "Cantidad": detalle.findtext("cantidad", default="").strip(),
                    "P. Unitario": detalle.findtext("precioUnitario", default="").strip(),
                    "Descuento": detalle.findtext("descuento", default="0.00").strip(),
                    "Total": detalle.findtext("precioTotalSinImpuesto", default="").strip(),
                    "Impuestos": "0.00"
                }
                
                # Extraer información de impuestos si existe
                impuestos = detalle.find(".//impuestos")
                if impuestos is not None:
                    for impuesto in impuestos.findall(".//impuesto"):
                        if impuesto.findtext("codigo", default="") == "2":  # IVA
                            producto["Impuestos"] = impuesto.findtext("valor", default="0.00").strip()
                
                detalles.append(producto)
            except Exception as e:
                logging.warning(f"Error extrayendo detalle: {str(e)}")
                continue
        
        return detalles
    
    except Exception as e:
        logging.error(f"Error en extraer_detalles_productos: {str(e)}")
        return []

def procesar_xml_a_detalles(xml_path):
    """Procesa un XML y devuelve los detalles de productos"""
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
            
            detalles = extraer_detalles_productos(comprobante_root, clave_acceso)
            return detalles

    except Exception as e:
        logging.error(f"Error al procesar el XML {xml_path}: {str(e)}")
        return []

def generar_archivo_detalles_productos():
    """Función principal para generar el archivo de detalles de productos"""
    try:
        configurar_carpetas()
        
        logging.info("Iniciando procesamiento de detalles de productos...")
        
        # Lista para acumular todos los detalles
        todos_detalles = []
        
        # Procesar todos los XML en la carpeta
        xml_procesados = 0
        productos_procesados = 0
        
        for archivo in os.listdir(CARPETA_XML_FACTURAS):
            if archivo.lower().endswith(".xml"):
                xml_path = os.path.join(CARPETA_XML_FACTURAS, archivo)
                try:
                    detalles = procesar_xml_a_detalles(xml_path)
                    if detalles:
                        todos_detalles.extend(detalles)
                        productos_procesados += len(detalles)
                        xml_procesados += 1
                except Exception as e:
                    logging.error(f"Error procesando {archivo}: {str(e)}")
                    continue
        
        # Crear DataFrame con todos los detalles
        if not todos_detalles:
            logging.warning("No se encontraron detalles de productos en los XML")
            return
        
        df_detalles = pd.DataFrame(todos_detalles)
        
        # Ordenar columnas
        column_order = [
            'CLAVE_ACCESO', 'RUC_EMISOR', 'RAZON_SOCIAL_EMISOR', 'FECHA_EMISION', 'Producto', 
            'Código', 'Cantidad', 'P. Unitario', 'Descuento', 'Total', 'Impuestos'
        ]
        df_detalles = df_detalles[column_order]
        
        # Generar nombre de archivo con fecha
        mes_actual = datetime.now().strftime("%m")
        año_actual = datetime.now().strftime("%Y")
        nombre_archivo = f"detalles_productos_{mes_actual}_{año_actual}.txt"
        ruta_salida = os.path.join(CARPETA_DETALLES, nombre_archivo)
        
        # Guardar el archivo
        df_detalles.to_csv(ruta_salida, sep="\t", index=False, encoding="utf-8")
        
        # Resumen de ejecución
        print("\n" + "="*50)
        print("RESUMEN DE EJECUCIÓN")
        print(f"- XMLs procesados: {xml_procesados}")
        print(f"- Productos encontrados: {productos_procesados}")
        print(f"- Archivo generado: {ruta_salida}")
        print("="*50)
        
        return ruta_salida
    
    except Exception as e:
        logging.error(f"ERROR CRÍTICO: {str(e)}", exc_info=True)
        raise
    
generar_archivo_detalles_productos()