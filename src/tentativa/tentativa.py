from datetime import datetime, timedelta

from src.quiz.quiz import Quiz
from src.usuario.aluno import Aluno
from src.papeis.participante import Participante
from src.tentativa.resposta import Resposta


class Tentativa:
    def __init__(self, participante, quiz):
        if not isinstance(participante, Participante):
            raise TypeError(
                "A tentativa deve pertencer a um Participante."
            )

        if not isinstance(quiz, Quiz):
            raise TypeError(
                "A tentativa deve estar associada a um Quiz."
            )

        if len(quiz) == 0:
            raise ValueError(
                "Não é possível responder um Quiz vazio."
            )

        # Verifica o limite individual de tentativas.
        tentativas_anteriores = [
            tentativa
            for tentativa in participante.tentativas
            if tentativa.quiz is quiz
        ]

        if (
            quiz.limite_tentativas is not None
            and len(tentativas_anteriores) >= quiz.limite_tentativas
        ):
            raise ValueError(
                "O participante atingiu o limite de tentativas deste Quiz."
            )

        self._participante = participante
        self._quiz = quiz
        self._data_inicio = datetime.now()
        self._data_fim = None
        self._respostas = {}
        self._status = "em andamento"

        # A primeira tentativa de um aluno congela o Quiz.
        if isinstance(participante, Aluno) and not quiz.congelado:
            quiz._congelar()

        participante.adicionar_tentativa(self)

    @property
    def participante(self):
        return self._participante

    @property
    def aluno(self):
        # Compatibilidade com códigos que utilizavam o nome antigo.
        return self._participante

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
    def status(self):
        return self._status

    @property
    def pontuacao(self):
        return sum(
            resposta.pontuacao
            for resposta in self._respostas.values()
        )

    @property
    def acertos(self):
        return sum(
            resposta.correta
            for resposta in self._respostas.values()
        )

    @property
    def quantidade_respondida(self):
        return len(self._respostas)

    @property
    def taxa_acerto(self):
        if not self._respostas:
            return 0

        return self.acertos / len(self._respostas) * 100

    @property
    def duracao(self):
        fim = self._data_fim or datetime.now()
        return (fim - self._data_inicio).total_seconds()

    @property
    def completa(self):
        return (
            self._status == "concluida"
            and len(self._respostas) == len(self._quiz)
        )

    def _verificar_tempo(self):
        if self._status != "em andamento":
            return

        limite = self._quiz.limite_tempo

        if limite is None:
            return

        tempo_decorrido = datetime.now() - self._data_inicio

        if tempo_decorrido >= timedelta(minutes=limite):
            self._encerrar("incompleta")

    def _encerrar(self, status):
        self._data_fim = datetime.now()
        self._status = status

    def registrar_resposta(self, indice_pergunta, indice_alternativa):
        if self._status != "em andamento":
            raise ValueError(
                "Essa tentativa já foi encerrada."
            )

        self._verificar_tempo()

        if self._status != "em andamento":
            raise ValueError(
                "O tempo limite foi atingido. A tentativa foi encerrada."
            )

        if type(indice_pergunta) is not int:
            raise TypeError(
                "O índice da pergunta deve ser inteiro."
            )

        if not 0 <= indice_pergunta < len(self._quiz):
            raise IndexError("Pergunta inexistente.")

        if indice_pergunta in self._respostas:
            raise ValueError(
                "Essa pergunta já foi respondida."
            )

        pergunta = self._quiz.perguntas[indice_pergunta]

        resposta = Resposta(
            pergunta,
            indice_alternativa
        )

        self._respostas[indice_pergunta] = resposta

        return resposta

    def finalizar(self):
        if self._status != "em andamento":
            raise ValueError(
                "Essa tentativa já foi encerrada."
            )

        self._verificar_tempo()

        if self._status != "em andamento":
            return

        if len(self._respostas) == len(self._quiz):
            self._encerrar("concluida")
        else:
            self._encerrar("incompleta")

    def __str__(self):
        return (
            f"Participante: {self.participante.nome}\n"
            f"Quiz: {self.quiz.titulo}\n"
            f"Status: {self.status}\n"
            f"Respostas registradas: {self.quantidade_respondida}\n"
            f"Pontuação: {self.pontuacao}\n"
            f"Taxa de acerto: {self.taxa_acerto:.2f}%"
        )
