
# SRI Scraper - Automatización de descarga de comprobantes electrónicos

Este proyecto automatiza el acceso al portal del SRI en línea para iniciar sesión con las credenciales del contribuyente, navegar hacia la sección de "Comprobantes Electrónicos Recibidos", y descargar los comprobantes en formatos `.txt`, `.xml` y `.pdf`. El sistema también permite extraer información de estos archivos y almacenarla en una base de datos Oracle 11g.

## 🧠 Objetivo

El objetivo principal es reducir el tiempo y esfuerzo necesarios para acceder manualmente a los comprobantes electrónicos en el portal del SRI, proporcionando una solución automatizada que permita:

- Iniciar sesión automáticamente en el SRI.
- Seleccionar el año, mes y tipo de comprobante deseado.
- Descargar los comprobantes en múltiples formatos.
- Extraer datos relevantes de los comprobantes descargados.
- Almacenar los datos en una base de datos para su posterior uso o análisis.

## ⚙️ ¿Cómo funciona?

La aplicación utiliza **Python** y la biblioteca **Playwright** para controlar el navegador de forma automatizada. El flujo principal del sistema es:

1. **Autenticación**: se ingresan las credenciales de usuario y se realiza el inicio de sesión en el portal del SRI.
2. **Navegación**: el script navega hacia la sección de comprobantes electrónicos.
3. **Selección del periodo**: el usuario elige el año, mes y tipo de comprobante desde la consola.
4. **Descarga**: el sistema automatiza la selección de filtros y descarga los comprobantes en formato `.pdf`, `.xml` y `.txt`.
5. **Persistencia**: los archivos descargados serán tratados posteriormente para extraer información y guardarla en Oracle.

## 📦 Estructura del proyecto

```
├── main.py
├── login.py
├── navigate.py
├── downloader.py
├── proceso_facturas_xml.py
├── proceso_retencion_xml.py
├── proceso_creditos_xml.py
└── proceso_liquidaciones_xml.py
```

## 🛠️ Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/sri-scraper.git
cd sri-scraper
```

2. **Crear un entorno virtual (opcional pero recomendado)**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
playwright install
```

## 🚀 Uso

Ejecuta el script principal con:

```bash
python main.py
```

Luego, sigue las instrucciones en consola para ingresar tus credenciales y seleccionar los comprobantes a descargar. El navegador se mantendrá abierto hasta que se completen las descargas.

## 📂 Archivos y Funcionalidad

### `main.py`
Archivo principal que ejecuta el flujo de trabajo del sistema.

### `login.py`
Automatiza el inicio de sesión con Playwright.

### `navigate.py`
Realiza la navegación por el menú del SRI hasta llegar a la sección de comprobantes.

### `downloader.py`
Controla la descarga de comprobantes XML y TXT, y gestiona la navegación paginada.

### `proceso_facturas_xml.py`
Procesa y estructura la información de facturas electrónicas.

### `proceso_retencion_xml.py`
Procesa comprobantes de retención.

### `proceso_creditos_xml.py`
Procesa notas de crédito electrónicas.

### `proceso_liquidaciones_xml.py`
Procesa comprobantes de liquidaciones.

## 🛡️ Consideraciones

- **Limitaciones Actuales:** El sistema se ve afectado por el uso de reCAPTCHA en el login del SRI.
- **Pendientes:** Implementar escritura a base de datos Oracle 12c.
- **Archivos generados:** Todos los archivos de salida están en formato `.txt`, codificados en UTF-8 y organizados por tipo de comprobante.

## 👤 Autor

Luis Adrián Ramos Guzmán  
Practicante de Desarrollo de Software  
Empresa: Planit
