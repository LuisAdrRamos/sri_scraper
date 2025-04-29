import pandas as pd
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog
import os

# Función para abrir el diálogo de selección múltiple de archivos
def seleccionar_multiples_archivos(titulo, filetypes):
    Tk().withdraw()
    return filedialog.askopenfilenames(title=titulo, filetypes=filetypes)

# Seleccionar el archivo .txt
reporte = filedialog.askopenfilename(title="Selecciona el archivo .txt con los comprobantes", filetypes=[("Archivos TXT", "*.txt")])

# Leer el archivo .txt
df = pd.read_csv(reporte, sep="\t", dtype=str, encoding="latin-1")

# Inicializar las columnas faltantes si no existen
for columna in ["VALOR_SIN_IMPUESTOS", "IVA", "IMPORTE_TOTAL"]:
    if columna not in df.columns:
        df[columna] = "nulo"

# Función para extraer datos directamente de cualquier parte del XML
def extraer_datos_desde_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Extraer el CDATA (comprobante real)
        comprobante_cdata = root.find(".//comprobante").text.strip()
        comprobante_root = ET.fromstring(comprobante_cdata)

        # Extraer clave de acceso
        clave_acceso = comprobante_root.find(".//claveAcceso").text

        # Inicializar valores por defecto
        valor_sin_impuestos = "0.00"
        iva = "0.00"
        importe_total = "0.00"

        # Buscar todas las combinaciones posibles
        base_tags = comprobante_root.findall(".//baseImponible")
        porcentaje_tags = comprobante_root.findall(".//porcentajeRetener")
        retenido_tags = comprobante_root.findall(".//valorRetenido")

        # Si las tres listas tienen al menos una etiqueta
        if base_tags and porcentaje_tags and retenido_tags:
            for base, porcentaje, retenido in zip(base_tags, porcentaje_tags, retenido_tags):
                if base.text not in ("0", "0.00", "", None):
                    valor_sin_impuestos = base.text
                    iva = porcentaje.text
                    importe_total = retenido.text
                    break

        return clave_acceso, valor_sin_impuestos, iva, importe_total

    except Exception as e:
        print(f"❌ Error al procesar el XML {xml_path}: {e}")
        return None, "nulo", "nulo", "nulo"


# Selección de todos los XML al inicio
xml_paths = list(seleccionar_multiples_archivos("Selecciona los archivos XML de comprobantes", [("Archivos XML", "*.xml")]))
xml_dict = {}

# Procesar todos los XML y mapear por clave de acceso
for xml_path in xml_paths:
    clave, _, _, _ = extraer_datos_desde_xml(xml_path)
    if clave:
        xml_dict[clave] = xml_path

# Función para validar y solicitar XMLs faltantes o incorrectos
def procesar_archivos():
    archivos_pendientes = True
    while archivos_pendientes:
        archivos_pendientes = False

        for idx, row in df.iterrows():
            clave_txt = row["CLAVE_ACCESO"]

            if clave_txt not in xml_dict:
                print(f"⚠️ No se encontró un XML para la clave de acceso: {clave_txt}")
                xml_path = filedialog.askopenfilename(title=f"Selecciona el XML para la clave {clave_txt}", filetypes=[("Archivos XML", "*.xml")])
                clave_xml, _, _, _ = extraer_datos_desde_xml(xml_path)

                if clave_xml and clave_xml == clave_txt:
                    xml_dict[clave_txt] = xml_path
                    print(f"✅ Archivo añadido para la clave: {clave_txt}")
                else:
                    print(f"❌ La clave del XML seleccionado ({clave_xml}) no coincide con la clave requerida ({clave_txt}). Intenta nuevamente.")
                    archivos_pendientes = True
                    break  # Volver a pedir todos los faltantes

# Ejecutar proceso de validación y carga
procesar_archivos()

# Actualizar el DataFrame con la información de los XMLs
for idx, row in df.iterrows():
    clave_txt = row["CLAVE_ACCESO"]
    xml_path = xml_dict.get(clave_txt)

    if xml_path:
        clave_xml, valor_sin_impuestos, iva, importe_total = extraer_datos_desde_xml(xml_path)

        if clave_xml == clave_txt:
            df.at[idx, "VALOR_SIN_IMPUESTOS"] = valor_sin_impuestos
            df.at[idx, "IVA"] = iva
            df.at[idx, "IMPORTE_TOTAL"] = importe_total
            print(f"✅ Datos actualizados para clave: {clave_txt}")
        else:
            print(f"⚠️ Clave de acceso del XML ({clave_xml}) no coincide con el registro ({clave_txt})")
    else:
        print(f"⚠️ No se encontró XML para la clave: {clave_txt}")

# Guardar el archivo actualizado
df.to_csv(reporte, sep="\t", index=False, encoding="latin-1")

print("\n✅ Proceso finalizado. El archivo TXT ha sido actualizado correctamente.")
