"""Tokens de design e geração da folha de estilo.

O QSS não tem variáveis. Por isso o arquivo estilo.qss usa marcadores
como $primaria, e este módulo troca cada marcador pelo valor do tema.
"""

from string import Template

from PySide6.QtCore import QSettings

from portaria.ui import ARQUIVO_ESTILO

PASTA_ICONES = ARQUIVO_ESTILO.with_name("icones")

TEMAS = {
    "claro": {
        "fundo": "#f6f7f9",
        "superficie": "#ffffff",
        "texto": "#1f2328",
        "texto_suave": "#57606a",
        "borda": "#868e96",
        "primaria": "#0b5ed7",
        "primaria_hover": "#0a58ca",
        "primaria_texto": "#ffffff",
        "perigo": "#b42318",
        "perigo_texto": "#ffffff",
        "foco": "#052c65",
        "aviso_fundo": "#e7f1ff",
        "aviso_borda": "#b6d4fe",
        "aviso_texto": "#052c65",
        "zebra": "#f3f6fa",
        "selecao": "#cfe2ff",
        "raio": "6px",
    },
    "escuro": {
        "fundo": "#1b1f24",
        "superficie": "#24292f",
        "texto": "#e6edf3",
        "texto_suave": "#9da7b3",
        "borda": "#768390",
        "primaria": "#4493f8",
        "primaria_hover": "#539bf5",
        "primaria_texto": "#0d1117",
        "perigo": "#f47067",
        "perigo_texto": "#0d1117",
        "foco": "#a5d6ff",
        "aviso_fundo": "#132339",
        "aviso_borda": "#1f4a7a",
        "aviso_texto": "#c9e1ff",
        "zebra": "#2a3038",
        "selecao": "#1f4a7a",
        "raio": "6px",
    },
}


def gerar_folha(nome_tema: str = "claro") -> str:
    """Troca cada $marcador do estilo.qss pelo valor do tema escolhido."""
    valores = dict(TEMAS[nome_tema])
    valores["tema"] = nome_tema                       # escolhe o ícone claro ou escuro
    valores["icones"] = PASTA_ICONES.as_posix()       # barras "/" também no Windows
    modelo = Template(ARQUIVO_ESTILO.read_text(encoding="utf-8"))
    return modelo.substitute(valores)


def _configuracoes() -> QSettings:
    return QSettings("Senac-PI", "PortariaDigital")


def tema_salvo() -> str:
    nome = _configuracoes().value("tema", "claro")
    return nome if nome in TEMAS else "claro"


def salvar_tema(nome_tema: str) -> None:
    _configuracoes().setValue("tema", nome_tema)


def contraste(cor_a: str, cor_b: str) -> float:
    """Razão de contraste WCAG entre duas cores hexadecimais (1 a 21)."""

    def luminancia(cor):
        cor = cor.lstrip("#")
        canais = [int(cor[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        lineares = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
        r, g, b = lineares
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    clara, escura = sorted((luminancia(cor_a), luminancia(cor_b)), reverse=True)
    return (clara + 0.05) / (escura + 0.05)
