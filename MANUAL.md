# Portaria Digital · Manual do operador

Este manual é para quem trabalha na recepção. Ele explica o uso diário do programa.

## Abrir o programa
Dê dois cliques em **PortariaDigital**. A janela abre na aba **Portaria**.
O programa funciona sem internet.

## Registrar a entrada de um visitante
1. Digite o **CPF** e aperte **Tab**.
2. Se a pessoa já veio antes, o nome aparece sozinho e fica bloqueado. Se é a primeira vez, digite o **nome completo**.
3. Escolha o **setor**. Entre parênteses aparece quantas pessoas já estão lá e o limite, por exemplo `Coordenação (2/3)`.
4. Se quiser, preencha o **motivo** da visita.
5. Clique em **Registrar entrada** (ou **Alt+R**).
6. Entregue o crachá indicado na mensagem, por exemplo "Entregue o crachá V-03".

## Registrar a saída
1. Na lista **No prédio agora**, clique na linha do visitante. Use o campo de filtro para achar pelo nome ou setor.
2. Recolha o crachá.
3. Clique em **Registrar saída da visita selecionada** (ou **Alt+S**).
4. Se o visitante foi embora **sem devolver o crachá**, marque antes **Crachá extraviado** e avise a coordenação. Esse crachá não será entregue de novo.

## Mensagens e o que fazer
| Mensagem | O que fazer |
| --- | --- |
| CPF inválido. Confira os 11 dígitos. | Peça o documento de novo e redigite. |
| Informe o nome do visitante. | Digite o nome completo. |
| Selecione o setor de destino. | Escolha um setor na lista. |
| (Nome) já está no prédio. Registre a saída antes. | A pessoa tem uma entrada aberta. Procure-a na lista e registre a saída, se ela realmente saiu. |
| (Setor) atingiu a lotação. | Peça ao visitante que aguarde uma saída daquele setor. |
| Não há crachá disponível. Aguarde uma devolução. | Espere alguém sair ou avise a coordenação. |
| Selecione uma visita na tabela. | Clique na linha do visitante antes de registrar a saída. |
| Não foi possível acessar o banco de dados. | Veja abaixo. |

## "Não foi possível acessar o banco de dados"
1. Não tente várias vezes seguidas. Confira na lista se a última operação foi registrada.
2. Feche outros programas que possam estar usando o banco e tente de novo depois de alguns segundos.
3. Se a mensagem continuar, anote o horário e avise o suporte. O suporte encontra os detalhes técnicos no arquivo de registro (portaria.log).
4. Enquanto isso, anote entradas e saídas em papel e registre no sistema quando ele voltar.

## Consultar o histórico
1. Abra a aba **Histórico** (Alt+H).
2. Escolha as datas **De** e **Até**, digite um nome ou setor se quiser e clique em **Filtrar**.
3. Quem ainda está no prédio aparece como "no prédio". A coluna **Min.** mostra quanto tempo a visita durou.
4. Abaixo da tabela aparece o resumo de visitas por setor.

## Setores
Na aba **Setores** (Alt+T):
- **Novo setor**: informe nome e lotação máxima e clique em **Salvar**.
- **Editar selecionado** (ou dois cliques na linha): mude nome, lotação ou situação.
- Para tirar um setor da lista de entrada sem perder o histórico, edite e desmarque **Setor ativo**. Não é possível desativar um setor com visitantes dentro.
- **Excluir selecionado** só funciona para setores que nunca receberam visitas. Os demais devem ser desativados.

## Tema escuro
Menu **Visualizar > Tema escuro** (Ctrl+T). O programa lembra a escolha.

## Cuidados com dados pessoais
- A tela mostra só parte do CPF. Não anote nem fotografe CPFs completos.
- Não deixe a tela aberta e sem ninguém no balcão.
- O banco fica no computador da recepção. Não copie o arquivo portaria.db para pen drives ou e-mail sem autorização da coordenação.
- Faça o backup combinado com a coordenação: com o programa fechado, copie o portaria.db para o local seguro indicado.
