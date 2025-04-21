
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
├── auth/
│   └── login.py
├── scraper/
│   ├── menu_usuario.py
│   └── navigate.py
├── main.py
├── requirements.txt
```

## 🛠️ Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/sri-scraper.git
cd sri-scraper
```

### 2. **Configurar variables de entorno**

Crea un archivo `.env` con tus credenciales del SRI:

```env
SRI_USER=tu_usuario
SRI_PASS=tu_contraseña
```

### 3. **Instalación de dependencias**

Este proyecto usa Python 3.8 o superior. A continuación se listan las librerías necesarias y su propósito:

| Librería         | Instalación                      | Descripción |
|------------------|----------------------------------|-------------|
| `playwright`     | `pip install playwright`         | Automatiza la navegación en el portal del SRI (simula un navegador, similar a Selenium pero más moderno). |
| `python-dotenv`  | `pip install python-dotenv`      | Permite cargar variables de entorno desde un archivo `.env` (por ejemplo, usuario y contraseña del contribuyente). |

Una vez instaladas, ejecuta también:

```bash
playwright install
```

Este comando descarga los navegadores necesarios (Chromium, Firefox, WebKit) para que Playwright pueda funcionar correctamente.


## 🚀 Uso

Ejecuta el script principal con:

```bash
python main.py
```

Luego, sigue las instrucciones en consola para ingresar tus credenciales y seleccionar los comprobantes a descargar. El navegador se mantendrá abierto hasta que se completen las descargas.

---

## 🛡️ Consideraciones

- Asegúrate de tener conexión estable a internet.
- Asegúrate de tener un RUC y constraseña en el .env
- Puedes modificar el flujo desde `main.py` para controlar el bucle de descargas.
- El proyecto está pensado para uso interno de automatización empresarial.

---

## 🔐 Licencia

Este proyecto ha sido desarrollado exclusivamente para uso interno dentro de la empresa Planit como parte de un sistema privado. Su distribución o reutilización fuera de este contexto no está permitida sin autorización expresa.

---
