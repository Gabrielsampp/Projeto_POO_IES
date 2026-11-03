
from src.usuario.usuario import Usuario


class Aluno(Usuario):
    def __init__(self, nome, email, matricula):
        super().__init__(nome, email, matricula)
        self._tentativas = []

    @property
    def tipo(self):
        return "Aluno"

    @property
    def tentativas(self):
        return tuple(self._tentativas)

    def adicionar_tentativa(self, tentativa):
        from src.tentativa.tentativa import Tentativa

        if not isinstance(tentativa, Tentativa):
            raise TypeError("É necessário fornecer uma Tentativa.")

        if tentativa.aluno is not self:
            raise ValueError("A tentativa pertence a outro aluno.")

        if tentativa in self._tentativas:
            raise ValueError("Essa tentativa já foi registrada.")

        self._tentativas.append(tentativa)

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"Total de tentativas: {len(self._tentativas)}"
        )
