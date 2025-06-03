import cx_Oracle
import pandas as pd
from datetime import datetime

def conectar_oracle():
    return cx_Oracle.connect("SYSTEM/root@localhost:1521/ORCL")  # Ajusta tus datos

def parse_fecha(fecha):
    try:
        return datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")
    except:
        return None

def parse_fecha_corta(fecha):
    try:
        return datetime.strptime(fecha, "%d/%m/%Y")
    except:
        return None

def insertar_comprobantes_txt(path_txt, nombre_tabla):
    df = pd.read_csv(path_txt, sep="\t")
    df = df.where(pd.notnull(df), None)

    df["FECHA_AUTORIZACION"] = df["FECHA_AUTORIZACION"].map(parse_fecha)
    df["FECHA_EMISION"] = df["FECHA_EMISION"].map(parse_fecha_corta)

    columnas = [
        "RUC_EMISOR", "RAZON_SOCIAL_EMISOR", "TIPO_COMPROBANTE",
        "SERIE_COMPROBANTE", "CLAVE_ACCESO", "FECHA_AUTORIZACION",
        "FECHA_EMISION", "IDENTIFICACION_RECEPTOR", "VALOR_SIN_IMPUESTOS",
        "IVA", "IMPORTE_TOTAL", "NUMERO_DOCUMENTO_MODIFICADO"
    ]

    columnas_bd = [f"FESRI_{col}" for col in columnas]
    placeholders = ", ".join([f":{i+1}" for i in range(len(columnas))])
    sql_insert = f"""
        INSERT INTO {nombre_tabla} ({', '.join(columnas_bd)})
        VALUES ({placeholders})
    """
    sql_check = f"SELECT COUNT(*) FROM {nombre_tabla} WHERE FESRI_CLAVE_ACCESO = :1"

    con = conectar_oracle()
    cur = con.cursor()
    insertados = 0
    ignorados = 0

    for row in df.itertuples(index=False):
        clave = getattr(row, "CLAVE_ACCESO", None)
        cur.execute(sql_check, [clave])
        existe = cur.fetchone()[0]

        if existe:
            ignorados += 1
            continue

        valores = [getattr(row, col, None) for col in columnas]
        cur.execute(sql_insert, valores)
        insertados += 1

    con.commit()
    cur.close()
    con.close()

    print(f"✅ Registros insertados: {insertados}")
    print(f"⚠️  Registros ignorados por clave repetida: {ignorados}")
