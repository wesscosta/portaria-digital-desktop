"""Onde a aplicação guarda os dados do usuário (banco e log)."""

from pathlib import Path

from PySide6.QtCore import QCoreApplication, QStandardPaths

ORGANIZACAO = "Senac-PI"
APLICACAO = "PortariaDigital"


def pasta_dados() -> Path:
    """Pasta persistente por usuário, a mesma para o app e para os scripts."""
    QCoreApplication.setOrganizationName(ORGANIZACAO)
    QCoreApplication.setApplicationName(APLICACAO)
    local = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppLocalDataLocation
    )
    if not local:
        raise RuntimeError("Diretório de dados não disponível.")
    pasta = Path(local)
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def caminho_banco() -> str:
    return str(pasta_dados() / "portaria.db")
