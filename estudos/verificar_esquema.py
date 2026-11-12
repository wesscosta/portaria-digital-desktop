import sqlite3
from pathlib import Path

conn = sqlite3.connect(":memory:")
conn.executescript(Path("portaria/schema.sql").read_text(encoding="utf-8"))

for tipo, nome in conn.execute(
    "SELECT type, name FROM sqlite_master "
    "WHERE name NOT LIKE 'sqlite_%' ORDER BY type DESC, name"
):
    print(tipo, nome)

print("chaves estrangeiras de visita:")
for fk in conn.execute("PRAGMA foreign_key_list(visita)"):
    print(" ", fk[3], "->", fk[2])
