# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [1.0.0] - 2026-11-12

### Adicionado
- Entrada de visitante com crachá automático, cadastro de visitante novo na mesma transação e campo de motivo.
- Saída com devolução do crachá ou registro de crachá extraviado.
- Lista de quem está no prédio, com filtro, CPF mascarado e contador de crachás.
- Lotação máxima por setor, com ocupação exibida no combo.
- Histórico por período, nome ou setor, com permanência em minutos e resumo por setor.
- Gestão de setores com diálogo, exclusão protegida e desativação.
- Persistência em SQLite com SQL explícito e parametrizado, índices parciais e chaves estrangeiras.
- Regras de negócio em `servicos.py` e SQL em `repositorio.py`.
- Tratamento central de falhas com aviso ao operador e log técnico sem dados pessoais.
- Temas claro e escuro com tokens, variantes de botão e componentes em português.
- Gerador de dados fictícios com semente e suíte de testes automatizados (pytest).
- Módulo ORM isolado (SQLAlchemy) para comparação com o SQL explícito.

### Corrigido
- CPF validado pelos dígitos verificadores, visitante não entra duas vezes e saída não repete sobre seleção antiga.
- Falha no meio da entrada não deixa visita, cadastro nem crachá parcialmente gravados.

### Limitações conhecidas
- Um computador por vez acessando o banco.
- CPFs dos dados fictícios podem coincidir com CPFs reais por acaso.
