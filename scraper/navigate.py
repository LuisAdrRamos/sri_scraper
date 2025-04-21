from playwright.sync_api import Page

def navegar_comprobantes(pagina: Page):
    try:
        print("Iniciando navegación hacia Comprobantes Electrónicos Recibidos...")

        # Paso 1: Clic en el botón del menú principal (abrir sidebar)
        print("Desplegando el menú principal...")
        
        # Espera hasta que el botón esté visible
        # pagina.wait_for_selector("button#sri-menu", state="visible", timeout=10000)  
        pagina.click("button#sri-menu")  # Ajusta el selector al botón principal del menú

        # Paso 2: Clic en "Facturación Electrónica"
        print("Accediendo a Facturación Electrónica...")
        # pagina.wait_for_selector("a.ui-panelmenu-header-link span.ui-menuitem-text:has-text('FACTURACIÓN ELECTRÓNICA')", state="visible", timeout=10000)
        pagina.click("a.ui-panelmenu-header-link span.ui-menuitem-text:has-text('FACTURACIÓN ELECTRÓNICA')")  # Selector refinado con el texto visible

        # Paso 3: Clic en "Comprobantes Electrónicos Recibidos"
        print("Accediendo a Comprobantes Electrónicos Recibidos...")
        # pagina.wait_for_selector("a.ui-menuitem-link span.ui-menuitem-text:has-text('Comprobantes electrónicos recibidos')", state="visible", timeout=10000)
        pagina.click("a.ui-menuitem-link span.ui-menuitem-text:has-text('Comprobantes electrónicos recibidos')")  # Selector refinado con el texto visible

        # Verificar que la nueva página se haya cargado correctamente
        # pagina.wait_for_url("**/tuportal-internet/accederAplicacion.jspa**", timeout=10000)
        print("Se ha accedido correctamente a la sección de Comprobantes Electrónicos Recibidos.")
        return True

    except Exception as e:
        print(f"Error durante la navegación: {e}")
        return False