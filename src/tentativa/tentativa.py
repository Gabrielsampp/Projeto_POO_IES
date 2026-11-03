
from datetime import datetime

from src.quiz.quiz import Quiz
from src.usuario.aluno import Aluno


class Tentativa:
    def __init__(self, aluno, quiz):
        if not isinstance(aluno, Aluno):
            raise TypeError("A tentativa deve pertencer a um Aluno.")

        if not isinstance(quiz, Quiz):
            raise TypeError("A tentativa deve estar associada a um Quiz.")

        if len(quiz) == 0:
            raise ValueError("Não é possível responder um Quiz vazio.")

        self._aluno = aluno
        self._quiz = quiz
        self._data_inicio = datetime.now()
        self._data_fim = None
        self._respostas = {}
        self._pontuacao = 0
        self._status = "em andamento"

    @property
    def aluno(self):
        return self._aluno

    @property
    def quiz(self):
        return self._quiz

    @property
    def data_inicio(self):
        return self._data_inicio

    @property
    def data_fim(self):
        return self._data_fim

    @property
    def respostas(self):
        return self._respostas.copy()

    @property
    def pontuacao(self):
        return self._pontuacao

    @property
    def status(self):
        return self._status

    def registrar_resposta(self, indice_pergunta, indice_alternativa):
        if self._status != "em andamento":
            raise ValueError("Essa tentativa já foi encerrada.")

        if type(indice_pergunta) is not int:
            raise TypeError("O índice da pergunta deve ser inteiro.")

        if not 0 <= indice_pergunta < len(self._quiz):
            raise IndexError("Pergunta inexistente.")

        if type(indice_alternativa) is not int:
            raise TypeError("O índice da alternativa deve ser inteiro.")

        pergunta = self._quiz.perguntas[indice_pergunta]

        if not 0 <= indice_alternativa < len(pergunta.alternativas):
            raise IndexError("Alternativa inexistente.")

        if indice_pergunta in self._respostas:
            raise ValueError("Essa pergunta já foi respondida.")

        self._respostas[indice_pergunta] = indice_alternativa

    def finalizar(self):
        if self._status != "em andamento":
            raise ValueError("Essa tentativa já foi encerrada.")

        self._data_fim = datetime.now()
        self._status = "concluida"

    def __str__(self):
        return (
            f"Aluno: {self.aluno.nome}\n"
            f"Quiz: {self.quiz.titulo}\n"
            f"Status: {self.status}\n"
            f"Respostas registradas: {len(self._respostas)}"
        )
