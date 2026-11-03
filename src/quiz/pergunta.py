from src.tema.tema import Tema


class Pergunta:
    def __init__(
        self, tema, enunciado, alternativas,
        indice_correto, dificuldade
    ):
        self.tema = tema
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.indice_correto = indice_correto
        self.dificuldade = dificuldade
        self._quiz = None

    @property
    def quiz(self):
        return self._quiz

    def _vincular_quiz(self, quiz):
        if self._quiz is not None and self._quiz is not quiz:
            raise ValueError(
                "Esta pergunta já pertence a outro Quiz."
            )

        self._quiz = quiz

    @property
    def tema(self):
        return self._tema

    @tema.setter
    def tema(self, valor):
        if not isinstance(valor, Tema):
            raise TypeError("É necessário fornecer um objeto Tema.")

        self._tema = valor

    @property
    def enunciado(self):
        return self._enunciado

    @enunciado.setter
    def enunciado(self, valor):
        if not isinstance(valor, str):
            raise TypeError("O enunciado deve ser um texto.")

        valor = valor.strip()

        if not valor:
            raise ValueError("O enunciado não pode estar vazio.")

        self._enunciado = valor

    @property
    def alternativas(self):
        return tuple(self._alternativas)

    @alternativas.setter
    def alternativas(self, valores):
        if not isinstance(valores, (list, tuple)):
            raise TypeError(
                "As alternativas devem ser uma lista ou tupla."
            )

        if not 3 <= len(valores) <= 5:
            raise ValueError(
                "A pergunta deve possuir entre 3 e 5 alternativas."
            )

        alternativas = []

        for valor in valores:
            if not isinstance(valor, str):
                raise TypeError("As alternativas devem ser textos.")

            valor = valor.strip()

            if not valor:
                raise ValueError(
                    "As alternativas não podem estar vazias."
                )

            if valor.casefold() in [
                item.casefold() for item in alternativas
            ]:
                raise ValueError(
                    "Não podem existir alternativas duplicadas."
                )

            alternativas.append(valor)

        if hasattr(self, "_indice_correto"):
            if self._indice_correto >= len(alternativas):
                raise ValueError(
                    "A alteração das alternativas invalidaria "
                    "o índice correto."
                )

        self._alternativas = alternativas

    @property
    def indice_correto(self):
        return self._indice_correto

    @indice_correto.setter
    def indice_correto(self, valor):
        if type(valor) is not int:
            raise TypeError("O índice correto deve ser inteiro.")

        if not 0 <= valor < len(self._alternativas):
            raise ValueError("Índice da alternativa correta inválido.")

        self._indice_correto = valor

    @property
    def dificuldade(self):
        return self._dificuldade

    @dificuldade.setter
    def dificuldade(self, valor):
        if not isinstance(valor, str):
            raise TypeError("A dificuldade deve ser um texto.")

        valor = valor.strip().upper()

        if valor not in ("F", "M", "D"):
            raise ValueError(
                "A dificuldade deve ser F, M ou D."
            )

        self._dificuldade = valor

    def adicionar_alternativa(self, alternativa):
        if len(self._alternativas) >= 5:
            raise ValueError(
                "A pergunta não pode possuir mais de 5 alternativas."
            )

        if not isinstance(alternativa, str):
            raise TypeError("A alternativa deve ser um texto.")

        alternativa = alternativa.strip()

        if not alternativa:
            raise ValueError("A alternativa não pode estar vazia.")

        if any(
            item.casefold() == alternativa.casefold()
            for item in self._alternativas
        ):
            raise ValueError("A alternativa já existe.")

        self._alternativas.append(alternativa)

    def remover_alternativa(self, indice):
        if type(indice) is not int:
            raise TypeError("O índice deve ser inteiro.")

        if not 0 <= indice < len(self._alternativas):
            raise IndexError("Índice de alternativa inválido.")

        if len(self._alternativas) <= 3:
            raise ValueError(
                "A pergunta deve possuir pelo menos 3 alternativas."
            )

        if indice == self._indice_correto:
            raise ValueError(
                "Não é possível remover a alternativa correta."
            )

        self._alternativas.pop(indice)

        if indice < self._indice_correto:
            self._indice_correto -= 1

    def alterar_alternativa(self, indice, alternativa):
        if type(indice) is not int:
            raise TypeError("O índice deve ser inteiro.")

        if not 0 <= indice < len(self._alternativas):
            raise IndexError("Índice de alternativa inválido.")

        if not isinstance(alternativa, str):
            raise TypeError("A alternativa deve ser um texto.")

        alternativa = alternativa.strip()

        if not alternativa:
            raise ValueError("A alternativa não pode estar vazia.")

        for i, existente in enumerate(self._alternativas):
            if (
                i != indice
                and existente.casefold() == alternativa.casefold()
            ):
                raise ValueError("A alternativa já existe.")

        self._alternativas[indice] = alternativa

    def verificar_resposta(self, indice):
        if type(indice) is not int:
            raise TypeError(
                "O índice da resposta deve ser inteiro."
            )

        if not 0 <= indice < len(self._alternativas):
            raise IndexError("Índice de alternativa inválido.")

        return indice == self.indice_correto

    def calcular_pontuacao(self):
        pesos = {"F": 1, "M": 2, "D": 3}
        return pesos[self.dificuldade]

    def __str__(self):
        return (
            f"Tema: {self.tema}\n"
            f"Enunciado: {self.enunciado}\n"
            f"Alternativas: {list(self.alternativas)}\n"
            f"Dificuldade: {self.dificuldade}"
        )

    def __eq__(self, outra):
        if not isinstance(outra, Pergunta):
            return NotImplemented

        return (
            self.enunciado.casefold() == outra.enunciado.casefold()
            and self.tema == outra.tema
        )
