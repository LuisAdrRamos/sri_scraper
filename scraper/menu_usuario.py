from playwright.sync_api import Page as pagina

def seleccionar_fecha():
    print("\nSelecciona el año: ")
    years = ["2021", "2022", "2023", "2024", "2025"]
    while True:
        try:
            for i, year in enumerate(years, 1):
                print(f"{i}. {year}")
            opcion = int(input("Opcion: "))
            if 1 <= opcion <= len(years):
                year = years[opcion - 1]
                break
            else:
                print("Opcion fuera del rango, intente de nuevo")
        except ValueError:
            print("Entrada invalida. Por favor ingrese una opcion valida")
    
    print("\nSeleccionar el Mes: ")
    meses = {
        "Enero": "1", "Febrero": "2", "Marzo": "3", "Abril": "4", "Mayo": "5", "Junio": "6",
        "Julio": "7", "Agosto": "8", "Septiembre": "9", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
    }
    while True:
        try:
            for i, mes in enumerate(meses.keys(), 1):
                print(f"{i}. {mes}")
            opcion = int(input("Opcion: "))
            if 1 <= opcion <= len(meses):
                mes = list(meses.values())[opcion - 1]
                break
            else:
                print("Opcion fuera de rango, intente de nuevo")
        except ValueError:
            print("Entrada invalida. Por favor ingrese una opcion valida")
    
    return year, mes


def seleccionar_comprobante():
    print("\nSeleccione el tipo de comprobante: ")
    comprobantes = {
        "Factura": "1",
        "Liquidación de compra de bienes o prestación de servicios": "2",
        "Nota de crédito": "3",
        "Nota de débito": "4",
        "Comprobante de retención": "6"
    }
    while True:
        try:
            for i, comprobante in enumerate(comprobantes.keys(), 1): 
                print(f"{i}. {comprobante}")
            opcion = int(input("Opcion: "))
            if 1 <= opcion <= len(comprobantes):
                comprobante_nombre = list(comprobantes.keys())[opcion - 1]
                comprobante_valor = comprobantes[comprobante_nombre]
                return comprobante_valor, comprobante_nombre
            else:
                print("Opcion fuera de rango, intente de nuevo")
        except ValueError:
            print("Entrada invalida. Por favor ingrese una opcion valida")


def automatizar_seleccion(year: str, mes: str, comprobante_valor: str, pagina):
    try:
        print("\nRellenando las opciones de búsqueda...")

        # Año
        print(f"Seleccionando año {year}")
        pagina.select_option("select#frmPrincipal\\:ano", year)  

        # Mes
        print(f"Seleccionando mes: {mes}")
        pagina.select_option("select#frmPrincipal\\:mes", mes)  

        # Día (todos)
        print("Seleccionando todos los días")
        pagina.select_option("select#frmPrincipal\\:dia", "0")  
        
        print(f"Valor de comprobante enviado: {comprobante_valor}")

        # Tipo de comprobante
        print("Activando el menú desplegable de tipo de comprobante...")
        pagina.click("select#frmPrincipal\\:cmbTipoComprobante")  # Clic previo en el <select>
        pagina.select_option("select#frmPrincipal\\:cmbTipoComprobante", comprobante_valor)

        # Botón de consultar
        print("Ejecutando la consulta...")
        pagina.click("button#frmPrincipal\\:btnConsultar")  

        print("Filtros seleccionados correctamente")
        return True

    except Exception as e:
        print(f"❌ Error al automatizar la selección: {e}")
        return False
