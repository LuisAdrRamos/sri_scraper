from playwright.sync_api import Page

def automatizar_seleccion(comprobante_valor: str, pagina: Page) -> bool:
    try:
        print("\nRellenando las opciones de búsqueda...")
        # Selecciona todos los días
        print("Seleccionando todos los días")
        pagina.select_option("select#frmPrincipal\\:dia", "0")
        # Tipo de comprobante
        print(f"Valor de comprobante enviado: {comprobante_valor}")
        pagina.click("select#frmPrincipal\\:cmbTipoComprobante")
        pagina.select_option("select#frmPrincipal\\:cmbTipoComprobante", comprobante_valor)
        # Botón de consultar
        print("Ejecutando la consulta...")
        pagina.click("button#frmPrincipal\\:btnConsultar")
        print("Filtros seleccionados correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al automatizar la selección: {e}")
        return False