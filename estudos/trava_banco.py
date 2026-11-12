import time

from portaria.db import conectar

conn = conectar()  # o mesmo banco que a aplicação usa
conn.execute("BEGIN EXCLUSIVE")
print("Banco travado por 30 segundos. Use a aplicação agora.")
time.sleep(30)
conn.rollback()
print("Banco liberado.")
