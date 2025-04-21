import cx_Oracle
from config import settings

conn = cx_Oracle.connect(
    user=settings.ORACLE_USER,
    password=settings.ORACLE_PASSWORD,
    dsn=settings.ORACLE_DSN
)
