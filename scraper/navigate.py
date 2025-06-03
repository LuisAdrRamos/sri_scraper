from playwright.sync_api import Page

def navegar_comprobantes(pagina: Page):
    try:
        print("Iniciando navegación hacia Comprobantes Electrónicos Recibidos...")
        
        pagina.wait_for_timeout(1000)
        # Intentar cerrar el popup de encuesta si está presente
        try:
            cerrar_encuesta = pagina.locator("span.fa.fa-fw.fa-close")
            if cerrar_encuesta.is_visible():
                print("Cerrando popup de encuesta...")
                cerrar_encuesta.click()
                pagina.wait_for_timeout(1000)  # Esperar breve para que se cierre
        except Exception as e:
            print(f"No se encontró popup de encuesta o no se pudo cerrar: {e}")
            
        print("Desplegando el menú principal...")
        pagina.click("button#sri-menu")

        print("Accediendo a Facturación Electrónica...")
        pagina.click("a.ui-panelmenu-header-link span.ui-menuitem-text:has-text('FACTURACIÓN ELECTRÓNICA')")  # Selector refinado con el texto visible

        print("Accediendo a Comprobantes Electrónicos Recibidos...")
        pagina.click("a.ui-menuitem-link span.ui-menuitem-text:has-text('Comprobantes electrónicos recibidos')")  # Selector refinado con el texto visible

        print("Se ha accedido correctamente a la sección de Comprobantes Electrónicos Recibidos.")
        return True

    except Exception as e:
        print(f"Error durante la navegación: {e}")
        return False