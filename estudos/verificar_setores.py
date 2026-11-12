from portaria import servicos
from portaria.db import conectar, preparar_banco
from portaria.erros import RegraNegocioError

conn = conectar(":memory:")
preparar_banco(conn)
biblioteca = servicos.salvar_setor(conn, "Biblioteca", 4)
print("criado:", biblioteca)
try:
    servicos.salvar_setor(conn, "LABORATÓRIO", 5)
except RegraNegocioError as erro:
    print("recusado:", erro)
servicos.registrar_entrada(conn, "52998224725", biblioteca, nome="Ana Lima")
try:
    servicos.excluir_setor(conn, biblioteca)
except RegraNegocioError as erro:
    print("recusado:", erro)
