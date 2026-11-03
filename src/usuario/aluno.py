
from src.usuario.usuario import Usuario
from src.papeis.participante import Participante


class Aluno(Usuario, Participante):
    def __init__(self, nome, email, matricula):
        Usuario.__init__(self, nome, email, matricula)
        Participante.__init__(self)

    @property
    def tipo(self):
        return "Aluno"

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"Total de tentativas: {len(self.tentativas)}"
        )
