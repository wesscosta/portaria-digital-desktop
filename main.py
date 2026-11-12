"""Ponto de entrada definitivo da Portaria Digital."""

import logging
import sys

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtWidgets import QApplication

from portaria.caminhos import pasta_dados
from portaria.db import conectar, preparar_banco
from portaria.ui.janela_principal import JanelaPrincipal
from portaria.ui.tema import gerar_folha, tema_salvo


def main() -> int:
    app = QApplication(sys.argv)

    # Banco e log pertencem aos dados persistentes do usuário,
    # não ao diretório do executável nem à pasta de trabalho atual.
    logging.basicConfig(
        filename=str(pasta_dados() / "portaria.log"),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    conn = conectar()  # sem argumento: banco na pasta de dados do usuário
    try:
        preparar_banco(conn)

        # Traduz os botões padrão da interface Qt.
        tradutor = QTranslator(app)
        pasta_traducoes = QLibraryInfo.path(
            QLibraryInfo.LibraryPath.TranslationsPath
        )
        if tradutor.load(
            QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil),
            "qtbase", "_", pasta_traducoes
        ):
            app.installTranslator(tradutor)

        app.setStyle("Fusion")
        app.setStyleSheet(gerar_folha(tema_salvo()))

        janela = JanelaPrincipal(conn)
        janela.show()
        return app.exec()
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
