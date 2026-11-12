# Portaria Digital

Aplicação desktop educacional de controle de visitantes, construída com Python e PySide6
para praticar programação orientada a eventos, SQL, transações, regras de negócio,
testes e empacotamento.

## Recursos
- entrada e saída com crachá automático;
- lista de presentes com filtro e lotação por setor;
- histórico com permanência e resumo por setor;
- gestão de setores com exclusão protegida;
- registro de crachá extraviado;
- dados fictícios e testes automatizados.

## Requisitos
- Python 3.11 ou superior (o laboratório usa 3.15)

## Executar
```bash
python -m venv .venv
```
Ative o ambiente virtual e:
```bash
python -m pip install -r requirements.txt
python main.py
```
## Dados
O banco (portaria.db) e o registro técnico (portaria.log) ficam na pasta de dados do usuário,
definida pelo sistema operacional (`QStandardPaths.AppLocalDataLocation`), e não na pasta do
programa:

- Windows: `C:\Users\<usuário>\AppData\Local\Senac-PI\PortariaDigital`
- Linux: `~/.local/share/Senac-PI/PortariaDigital`
- macOS: `~/Library/Application Support/Senac-PI/PortariaDigital`

Para confirmar o local nesta máquina:
```bash
python -c "from portaria.caminhos import caminho_banco; print(caminho_banco())"
```
Para fazer backup, feche a aplicação e copie o portaria.db dessa pasta. O aplicativo, o
gerador de dados fictícios e `estudos/trava_banco.py` usam esse mesmo arquivo.

## Dados de demonstração
```bash
python dados_ficticios.py --semente 7
```

## Testes
```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Executável
```bash
python -m pip install -r requirements-dev.txt
pyinstaller --name PortariaDigital --windowed --add-data "portaria/schema.sql:portaria" --add-data "portaria/ui/estilo.qss:portaria/ui" --add-data "portaria/ui/icones:portaria/ui/icones" main.py
```
O programa fica em `dist/PortariaDigital/`. Gere-o no mesmo sistema operacional em que ele vai
rodar: um executável gerado no Linux não abre no Windows.

## Arquitetura
interface (portaria/ui) → serviços (regras e transações) → repositório (SQL) → SQLite

## Arquivos de estudo
Os scripts de laboratório ficam na pasta `estudos/`, dentro do repositório. Eles registram
experimentos que a turma refaz e cita na defesa técnica (SQL injection, transações, ORM,
chaves estrangeiras, banco travado, estilo), mas não fazem parte do programa: `main.py` não
os importa e o executável não os inclui. Execute-os a partir da raiz, por exemplo
`python -m estudos.comparar_orm`. Alguns gravam no `./portaria.db` de laboratório.

## Limitações conhecidas
- um computador por vez acessando o banco;
- CPFs dos dados fictícios podem coincidir com CPFs reais por acaso.

## Licenças
Código sob a licença MIT (arquivo LICENSE). PySide6 é distribuído sob LGPLv3 ou licença
comercial; este projeto usa a LGPLv3. Quem distribuir o programa deve manter o PySide6/Qt
como biblioteca separada e substituível pelo usuário, entregar o texto da LGPL e indicar onde
obter o código-fonte do Qt, além de publicar qualquer alteração feita no próprio Qt.
Detalhes: https://www.qt.io/licensing/
