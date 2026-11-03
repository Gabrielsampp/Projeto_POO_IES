
from src.usuario.usuario import Usuario
from src.papeis.participante import Participante
from src.papeis.criador import Criador


class Professor(Usuario, Participante, Criador):
    def __init__(self, nome, email, identificador):
        Usuario.__init__(self, nome, email, identificador)
        Participante.__init__(self)
        Criador.__init__(self)

    @property
    def tipo(self):
        return "Professor"

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"Quizzes cadastrados: {len(self.quizzes)}\n"
            f"Total de tentativas: {len(self.tentativas)}"
        )
