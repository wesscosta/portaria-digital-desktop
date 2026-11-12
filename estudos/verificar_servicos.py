from portaria import servicos
from portaria.db import conectar, preparar_banco
from portaria.erros import RegraNegocioError

conn = conectar(":memory:")
preparar_banco(conn)
coord = conn.execute("SELECT id FROM setor WHERE nome = 'Coordenação'").fetchone()[0]

for cpf in ["52998224725", "11144477735", "39053344705", "15350946056"]:
    try:
        servicos.registrar_entrada(conn, cpf, coord, nome="Teste")
        print("entrou", cpf)
    except RegraNegocioError as erro:
        print("recusado:", erro)

try:
    servicos.registrar_entrada(conn, "123", coord, nome="Teste")
except RegraNegocioError as erro:
    print("recusado:", erro, "| campo:", erro.campo)
