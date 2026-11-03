
from src.usuario.usuario import Usuario
from src.papeis.participante import Participante
from src.quiz.quiz import Quiz


class Professor(Usuario, Participante):
    def __init__(self, nome, email, identificador):
        Usuario.__init__(self, nome, email, identificador)
        Participante.__init__(self)
        self._quizzes = []

    @property
    def tipo(self):
        return "Professor"

    @property
    def quizzes(self):
        return tuple(self._quizzes)

    def adicionar_quiz(self, quiz):
        if not isinstance(quiz, Quiz):
            raise TypeError("É necessário fornecer um objeto Quiz.")

        if quiz in self._quizzes:
            raise ValueError("Esse Quiz já está associado ao professor.")

        if quiz.professor is not None and quiz.professor is not self:
            raise ValueError("Esse Quiz já pertence a outro professor.")

        quiz.professor = self
        self._quizzes.append(quiz)

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"Quizzes cadastrados: {len(self._quizzes)}\n"
            f"Total de tentativas: {len(self.tentativas)}"
        )
