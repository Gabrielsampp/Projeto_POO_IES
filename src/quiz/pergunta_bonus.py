from src.quiz.pergunta import Pergunta


class PerguntaBonus(Pergunta):
    """Pergunta que concede 2 pontos adicionais."""

    def calcular_pontuacao(self):
        return super().calcular_pontuacao() + 2