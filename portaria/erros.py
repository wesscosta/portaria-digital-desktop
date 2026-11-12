class RegraNegocioError(Exception):
    """Erro previsto do usuário ou do processo.

    A mensagem é exibida na interface. Erros de programação e de banco
    NÃO usam esta classe.
    """

    def __init__(self, mensagem: str, campo: str | None = None):
        super().__init__(mensagem)
        self.campo = campo  # "cpf" ou "nome": qual campo a interface deve focar
