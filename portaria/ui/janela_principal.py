import logging
import sqlite3

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStyle,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from portaria import repositorio as repo
from portaria import servicos
from portaria.erros import RegraNegocioError
from portaria.validacao import mascarar_documento, normalizar_documento
from portaria.ui.dialogo_setor import DialogoSetor
from portaria.ui.tema import gerar_folha, salvar_tema, tema_salvo

log = logging.getLogger(__name__)
FALHA = object()  # sinal de que a operação falhou e o usuário já foi avisado
COLUNAS = ["Visita", "Nome", "CPF", "Setor", "Crachá", "Entrada"]
COLUNAS_HISTORICO = ["Visita", "Nome", "CPF", "Setor", "Crachá", "Entrada", "Saída", "Min."]
COLUNAS_SETORES = ["Código", "Setor", "Lotação", "Situação", "Visitas registradas"]


def nova_tabela(colunas):
    tabela = QTableWidget(0, len(colunas))
    tabela.setHorizontalHeaderLabels(colunas)
    tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
    tabela.setSelectionMode(QAbstractItemView.SingleSelection)
    tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
    tabela.verticalHeader().setVisible(False)
    tabela.setAlternatingRowColors(True)
    return tabela


def estilizar_botao(botao, variante=None, icone=None):
    """Cursor de mão, variante visual da folha de estilo e ícone opcional."""
    botao.setCursor(Qt.CursorShape.PointingHandCursor)
    if variante:
        botao.setProperty("variante", variante)
    if icone is not None:
        botao.setIcon(botao.style().standardIcon(icone))
    return botao


def preencher_tabela(tabela, linhas):
    tabela.setRowCount(len(linhas))
    for i, valores in enumerate(linhas):
        for j, valor in enumerate(valores):
            tabela.setItem(i, j, QTableWidgetItem("" if valor is None else str(valor)))
    tabela.setCurrentCell(-1, -1)


class JanelaPrincipal(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.setWindowTitle("Portaria Digital")
        self.resize(900, 560)

        abas = QTabWidget()
        abas.addTab(self.montar_aba_portaria(), "&Portaria")
        abas.addTab(self.montar_aba_historico(), "&Histórico")
        abas.addTab(self.montar_aba_setores(), "Se&tores")
        abas.currentChanged.connect(lambda _indice: self.atualizar_tudo())
        self.setCentralWidget(abas)
        self.montar_menu()

        self.atualizar_tudo()

    def montar_aba_portaria(self):
        # ---------- formulário de entrada ----------
        self.campo_cpf = QLineEdit()
        self.campo_cpf.setPlaceholderText("Somente números")
        self.campo_cpf.setMaxLength(14)
        self.campo_nome = QLineEdit()
        self.combo_setor = QComboBox()
        self.campo_motivo = QLineEdit()
        self.campo_motivo.setPlaceholderText("Opcional")
        self.botao_entrada = QPushButton("&Registrar entrada")
        estilizar_botao(self.botao_entrada, "primario",
                        QStyle.StandardPixmap.SP_DialogApplyButton)
        self.botao_limpar = QPushButton("&Limpar campos")
        estilizar_botao(self.botao_limpar)
        self.mensagem = QLabel("Informe o CPF do visitante.")
        self.mensagem.setObjectName("mensagem")

        formulario = QFormLayout()
        formulario.addRow("&CPF:", self.campo_cpf)
        formulario.addRow("&Nome:", self.campo_nome)
        formulario.addRow("S&etor:", self.combo_setor)
        formulario.addRow("&Motivo:", self.campo_motivo)

        botoes = QHBoxLayout()
        botoes.addWidget(self.botao_entrada)
        botoes.addWidget(self.botao_limpar)

        # ---------- quem está no prédio ----------
        self.campo_filtro = QLineEdit()
        self.campo_filtro.setPlaceholderText("Filtrar por nome ou setor")
        self.tabela = nova_tabela(COLUNAS)
        self.botao_saida = QPushButton("Registrar &saída da visita selecionada")
        estilizar_botao(self.botao_saida)
        self.check_extraviado = QCheckBox("Crachá e&xtraviado (não devolvido)")
        self.contador = QLabel()

        layout = QVBoxLayout()
        layout.addLayout(formulario)
        layout.addLayout(botoes)
        layout.addWidget(self.mensagem)
        layout.addWidget(QLabel("No prédio agora:"))
        layout.addWidget(self.campo_filtro)
        layout.addWidget(self.tabela)
        layout.addWidget(self.check_extraviado)
        layout.addWidget(self.botao_saida)
        layout.addWidget(self.contador)

        # ---------- eventos ----------
        self.campo_cpf.editingFinished.connect(self.buscar_visitante)
        self.botao_entrada.clicked.connect(self.registrar_entrada)
        self.botao_limpar.clicked.connect(self.limpar_campos)
        self.botao_saida.clicked.connect(self.registrar_saida)
        self.campo_filtro.textChanged.connect(self.atualizar_tabela)

        aba = QWidget()
        aba.setLayout(layout)
        return aba

    def montar_aba_historico(self):
        hoje = QDate.currentDate()
        self.data_inicio = QDateEdit(hoje.addDays(-7))
        self.data_fim = QDateEdit(hoje)
        for campo in (self.data_inicio, self.data_fim):
            campo.setCalendarPopup(True)
            campo.setDisplayFormat("dd/MM/yyyy")
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Nome ou setor")
        botao_filtrar = estilizar_botao(QPushButton("&Filtrar"))
        self.tabela_historico = nova_tabela(COLUNAS_HISTORICO)
        self.resumo = QLabel()
        self.resumo.setWordWrap(True)

        botao_filtrar.clicked.connect(self.atualizar_historico)
        self.campo_busca.returnPressed.connect(self.atualizar_historico)

        filtros = QHBoxLayout()
        filtros.addWidget(QLabel("De:"))
        filtros.addWidget(self.data_inicio)
        filtros.addWidget(QLabel("Até:"))
        filtros.addWidget(self.data_fim)
        filtros.addWidget(self.campo_busca, 1)
        filtros.addWidget(botao_filtrar)

        layout = QVBoxLayout()
        layout.addLayout(filtros)
        layout.addWidget(self.tabela_historico)
        layout.addWidget(self.resumo)
        aba = QWidget()
        aba.setLayout(layout)
        return aba

    def montar_aba_setores(self):
        self.tabela_setores = nova_tabela(COLUNAS_SETORES)
        self._setores = []
        botao_novo = estilizar_botao(QPushButton("&Novo setor"), "primario")
        botao_editar = estilizar_botao(QPushButton("E&ditar selecionado"))
        botao_excluir = estilizar_botao(QPushButton("E&xcluir selecionado"), "perigo",
                                        QStyle.StandardPixmap.SP_TrashIcon)

        botao_novo.clicked.connect(self.novo_setor)
        botao_editar.clicked.connect(self.editar_setor)
        botao_excluir.clicked.connect(self.excluir_setor)
        self.tabela_setores.doubleClicked.connect(lambda _indice: self.editar_setor())

        botoes = QHBoxLayout()
        botoes.addWidget(botao_novo)
        botoes.addWidget(botao_editar)
        botoes.addWidget(botao_excluir)
        botoes.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(botoes)
        layout.addWidget(self.tabela_setores)
        aba = QWidget()
        aba.setLayout(layout)
        return aba

    def montar_menu(self):
        menu = self.menuBar().addMenu("&Visualizar")
        self.acao_tema_escuro = QAction("Tema &escuro", self)
        self.acao_tema_escuro.setCheckable(True)
        self.acao_tema_escuro.setShortcut("Ctrl+T")
        self.acao_tema_escuro.setChecked(tema_salvo() == "escuro")
        self.acao_tema_escuro.toggled.connect(self.trocar_tema)
        menu.addAction(self.acao_tema_escuro)

    def trocar_tema(self, escuro):
        nome = "escuro" if escuro else "claro"
        QApplication.instance().setStyleSheet(gerar_folha(nome))
        salvar_tema(nome)

    def atualizar_setores(self):
        setores = self._executar(repo.listar_setores, self.conn)
        if setores is FALHA:
            return False
        self._setores = setores
        preencher_tabela(self.tabela_setores, [
            [s["id"], s["nome"], s["lotacao_maxima"],
             "Ativo" if s["ativo"] else "Inativo", s["total_visitas"]]
            for s in setores
        ])
        return True

    def setor_selecionado(self):
        linha = self.tabela_setores.currentRow()
        if linha < 0:
            self._avisar("Selecione um setor na tabela.")
            return None
        setor_id = int(self.tabela_setores.item(linha, 0).text())
        return next((s for s in self._setores if s["id"] == setor_id), None)

    def novo_setor(self):
        dialogo = DialogoSetor(self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            dados = dialogo.dados()
            if self._executar(servicos.salvar_setor, self.conn, dados["nome"],
                              dados["lotacao_maxima"]) is not FALHA:
                self.atualizar_tudo()

    def editar_setor(self):
        setor = self.setor_selecionado()
        if setor is None:
            return
        dialogo = DialogoSetor(self, setor)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            dados = dialogo.dados()
            if self._executar(servicos.salvar_setor, self.conn, dados["nome"],
                              dados["lotacao_maxima"], dados["ativo"],
                              setor["id"]) is not FALHA:
                self.atualizar_tudo()

    def excluir_setor(self):
        setor = self.setor_selecionado()
        if setor is None:
            return
        resposta = QMessageBox.question(
            self, "Portaria Digital", f"Excluir o setor {setor['nome']}?"
        )
        if resposta != QMessageBox.StandardButton.Yes:
            return
        if self._executar(servicos.excluir_setor, self.conn, setor["id"]) is not FALHA:
            self.atualizar_tudo()

    def carregar_setores(self):
        setores = self._executar(repo.listar_setores_ativos, self.conn)
        if setores is FALHA:
            return False

        opcoes = []
        for setor in setores:
            ocupacao = self._executar(
                repo.contar_presentes_no_setor, self.conn, setor["id"]
            )
            if ocupacao is FALHA:
                return False
            opcoes.append((
                f"{setor['nome']} ({ocupacao}/{setor['lotacao_maxima']})",
                setor["id"]
            ))

        selecionado = self.combo_setor.currentData()
        self.combo_setor.clear()
        self.combo_setor.addItem("Selecione um setor", None)
        for rotulo, setor_id in opcoes:
            self.combo_setor.addItem(rotulo, setor_id)
        self.combo_setor.setCurrentIndex(
            max(self.combo_setor.findData(selecionado), 0)
        )
        return True

    def buscar_visitante(self):
        cpf = normalizar_documento(self.campo_cpf.text())
        visitante = self._executar(repo.buscar_visitante_por_documento, self.conn, cpf)
        if visitante is FALHA:
            return
        if visitante:
            self.campo_nome.setText(visitante["nome"])
            self.campo_nome.setReadOnly(True)
            self.mensagem.setText("Visitante já cadastrado. Escolha o setor.")
        else:
            if self.campo_nome.isReadOnly():
                self.campo_nome.clear()
            self.campo_nome.setReadOnly(False)

    def registrar_entrada(self):
        documento = self.campo_cpf.text()
        setor_id = self.combo_setor.currentData()
        if setor_id is None:
            self._avisar("Selecione o setor de destino.")
            return

        visita_id = self._executar(
            servicos.registrar_entrada, self.conn, documento, setor_id,
            nome=self.campo_nome.text(), motivo=self.campo_motivo.text(),
        )
        if visita_id is FALHA:
            self.mensagem.setText("Entrada não registrada. Leia o aviso e tente de novo.")
            return
        visita = self._executar(repo.obter_visita, self.conn, visita_id)
        self.limpar_campos()
        if visita is FALHA:
            self.mensagem.setText("Entrada registrada. Confira o crachá na tabela.")
        else:
            self.mensagem.setText(f"Entrada registrada. Entregue o crachá {visita['cracha']}.")
        self.atualizar_tudo()

    def registrar_saida(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            self._avisar("Selecione uma visita na tabela.")
            return
        visita_id = int(self.tabela.item(linha, 0).text())
        extraviado = self.check_extraviado.isChecked()
        if self._executar(servicos.registrar_saida, self.conn, visita_id,
                          extraviado=extraviado) is FALHA:
            return
        self.check_extraviado.setChecked(False)
        if extraviado:
            self.mensagem.setText("Saída registrada. Crachá marcado como extraviado.")
        else:
            self.mensagem.setText("Saída registrada. Crachá devolvido.")
        self.atualizar_tudo()

    def atualizar_tudo(self):
        """Para na primeira falha: banco indisponível gera um único alerta."""
        return (
            self.carregar_setores()
            and self.atualizar_tabela()
            and self.atualizar_historico()
            and self.atualizar_setores()
        )

    def focar_campo(self, campo):
        """Leva o cursor ao campo indicado pela regra que falhou."""
        widgets = {"cpf": self.campo_cpf, "nome": self.campo_nome}
        if campo in widgets:
            widgets[campo].setFocus()

    def atualizar_tabela(self):
        presentes = self._executar(repo.listar_presentes, self.conn)
        if presentes is FALHA:
            return False
        crachas = self._executar(repo.contar_crachas_por_situacao, self.conn)
        if crachas is FALHA:
            return False

        termo = self.campo_filtro.text().strip().lower()
        preencher_tabela(self.tabela, [
            [
                visita["id"], visita["nome"],
                mascarar_documento(visita["documento"]),
                visita["setor"], visita["cracha"], visita["entrada"]
            ]
            for visita in presentes
            if termo in f"{visita['nome']} {visita['setor']}".lower()
        ])
        self.contador.setText(
            f"No prédio: {len(presentes)} | "
            f"Crachás livres: {crachas.get('disponivel', 0)} | "
            f"Extraviados: {crachas.get('extraviado', 0)}"
        )
        return True

    def atualizar_historico(self):
        inicio = self.data_inicio.date().toString("yyyy-MM-dd")
        fim = self.data_fim.date().toString("yyyy-MM-dd")
        linhas = self._executar(
            repo.listar_historico, self.conn, inicio, fim,
            self.campo_busca.text()
        )
        if linhas is FALHA:
            return False
        resumo = self._executar(
            repo.resumo_por_setor, self.conn, inicio, fim
        )
        if resumo is FALHA:
            return False

        preencher_tabela(self.tabela_historico, [
            [
                visita["id"], visita["nome"],
                mascarar_documento(visita["documento"]), visita["setor"],
                visita["cracha"], visita["entrada"],
                visita["saida"] or "no prédio", visita["minutos"]
            ]
            for visita in linhas
        ])
        partes = []
        for setor in resumo:
            texto = f"{setor['setor']}: {setor['visitas']} visita(s)"
            if setor["media_minutos"] is not None:
                texto += f", média de {setor['media_minutos']} min"
            partes.append(texto)
        self.resumo.setText("Resumo do período. " + "; ".join(partes))
        return True

    def limpar_campos(self):
        self.campo_cpf.clear()
        self.campo_nome.clear()
        self.campo_nome.setReadOnly(False)
        self.campo_motivo.clear()
        self.combo_setor.setCurrentIndex(0)
        self.campo_cpf.setFocus()

    def _executar(self, funcao, *args, **kwargs):
        """Ponto único de tratamento de exceções da interface.

        Erro de regra: mensagem clara para o operador.
        Erro de banco: registro técnico no log e aviso genérico, sem expor
        detalhes internos nem dados pessoais.
        """
        try:
            return funcao(*args, **kwargs)
        except RegraNegocioError as erro:
            self._avisar(str(erro))
            self.focar_campo(erro.campo)
        except sqlite3.Error:
            log.exception("Falha de banco em %s", getattr(funcao, "__name__", "operação"))
            QMessageBox.critical(
                self, "Portaria Digital",
                "Não foi possível acessar o banco de dados. "
                "Confira a operação antes de tentar novamente ou avise o suporte.",
            )
        return FALHA

    def _avisar(self, texto):
        self.statusBar().showMessage(texto, 8000)  # some depois de 8 segundos
        QMessageBox.warning(self, "Portaria Digital", texto)
