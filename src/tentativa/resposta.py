from src.quiz.pergunta import Pergunta


class Resposta:
    def __init__(self, pergunta, indice_alternativa):
        if not isinstance(pergunta, Pergunta):
            raise TypeError("É necessário fornecer uma Pergunta.")

        if type(indice_alternativa) is not int:
            raise TypeError("O índice da alternativa deve ser inteiro.")

        if not 0 <= indice_alternativa < len(pergunta.alternativas):
            raise IndexError("Alternativa inexistente.")

        self._pergunta = pergunta
        self._indice_alternativa = indice_alternativa

    @property
    def pergunta(self):
        return self._pergunta

    @property
    def indice_alternativa(self):
        return self._indice_alternativa

    @property
    def correta(self):
        return self.pergunta.verificar_resposta(
            self.indice_alternativa
        )

    @property
    def pontuacao(self):
        if self.correta:
            return self.pergunta.calcular_pontuacao()

        return 0

    def __str__(self):
        resultado = "Correta" if self.correta else "Incorreta"

        return (
            f"Pergunta: {self.pergunta.enunciado}\n"
            f"Alternativa escolhida: {self.indice_alternativa}\n"
            f"Resultado: {resultado}\n"
            f"Pontuação: {self.pontuacao}"
        )
