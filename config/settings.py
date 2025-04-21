from dotenv import load_dotenv
import os

# Carga el .env
load_dotenv()

# SRI
SRI_RUC = os.getenv("SRI_RUC")
SRI_PASSWORD = os.getenv("SRI_PASSWORD")

# Oracle
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")

# Configuración general
HEADLESS = os.getenv("HEADLESS", "True") == "True"
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads/")
