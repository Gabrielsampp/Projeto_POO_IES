from src.quiz.pergunta import Pergunta


class Quiz:
    def __init__(
        self,
        titulo,
        perguntas=None,
        limite_tempo=None,
        limite_tentativas=None,
        valor_bonus=0,
        professor=None
    ):
        self._congelado = False

        self.titulo = titulo
        self.limite_tempo = limite_tempo
        self.limite_tentativas = limite_tentativas
        self.valor_bonus = valor_bonus
        self.professor = professor

        self._perguntas = []

        if perguntas is not None:
            if not isinstance(perguntas, (list, tuple)):
                raise TypeError(
                    "As perguntas devem estar em uma lista ou tupla."
                )

            for pergunta in perguntas:
                self.adicionar_pergunta(pergunta)

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        self._verificar_edicao()

        if not isinstance(valor, str):
            raise TypeError("O título deve ser um texto.")

        valor = valor.strip()

        if not valor:
            raise ValueError("O título não pode estar vazio.")

        self._titulo = valor

    @property
    def perguntas(self):
        return tuple(self._perguntas)

    @property
    def limite_tempo(self):
        return self._limite_tempo

    @limite_tempo.setter
    def limite_tempo(self, valor):
        self._verificar_edicao()

        if valor is not None:
            if type(valor) not in (int, float):
                raise TypeError(
                    "O limite de tempo deve ser numérico."
                )

            if valor <= 0:
                raise ValueError(
                    "O limite de tempo deve ser maior que zero."
                )

        self._limite_tempo = valor

    @property
    def limite_tentativas(self):
        return self._limite_tentativas

    @limite_tentativas.setter
    def limite_tentativas(self, valor):
        self._verificar_edicao()

        if valor is not None:
            if type(valor) is not int:
                raise TypeError(
                    "O limite de tentativas deve ser inteiro."
                )

            if valor <= 0:
                raise ValueError(
                    "O limite de tentativas deve ser maior que zero."
                )

        self._limite_tentativas = valor

    @property
    def valor_bonus(self):
        return self._valor_bonus

    @valor_bonus.setter
    def valor_bonus(self, valor):
        self._verificar_edicao()

        if type(valor) not in (int, float):
            raise TypeError(
                "O valor do bônus deve ser numérico."
            )

        if valor < 0:
            raise ValueError(
                "O valor do bônus não pode ser negativo."
            )

        self._valor_bonus = valor

    @property
    def congelado(self):
        return self._congelado

    def _verificar_edicao(self):
        if self._congelado:
            raise ValueError(
                "Este Quiz não pode mais ser alterado."
            )

    def adicionar_pergunta(self, pergunta):
        self._verificar_edicao()

        if not isinstance(pergunta, Pergunta):
            raise TypeError(
                "É necessário adicionar um objeto Pergunta."
            )

        if pergunta in self._perguntas:
            raise ValueError(
                "Esta pergunta já está no Quiz."
            )

        pergunta._vincular_quiz(self)
        self._perguntas.append(pergunta)

    def remover_pergunta(self, pergunta):
        self._verificar_edicao()

        for indice, existente in enumerate(self._perguntas):
            if existente is pergunta:
                self._perguntas.pop(indice)
                return

        raise ValueError(
            "A pergunta não pertence a este Quiz."
        )

    def alterar_ordem_perguntas(self, nova_ordem):
        self._verificar_edicao()

        if not isinstance(nova_ordem, (list, tuple)):
            raise TypeError(
                "A nova ordem deve ser uma lista ou tupla."
            )

        if len(nova_ordem) != len(self._perguntas):
            raise ValueError(
                "A nova ordem deve possuir todas as perguntas do Quiz."
            )

        if {
            id(pergunta) for pergunta in nova_ordem
        } != {
            id(pergunta) for pergunta in self._perguntas
        }:
            raise ValueError(
                "A nova ordem deve conter exatamente as perguntas do Quiz."
            )

        self._perguntas = list(nova_ordem)

    def calcular_pontuacao_maxima(self):
        return sum(
            pergunta.calcular_pontuacao()
            for pergunta in self._perguntas
    )

    def _congelar(self):
        if not self._perguntas:
            raise ValueError(
                "Não é possível iniciar um Quiz sem perguntas."
            )

        self._congelado = True

    def __len__(self):
        return len(self._perguntas)

    def __iter__(self):
        return iter(self._perguntas)

    def __str__(self):
        return (
            f"Quiz: {self.titulo}\n"
            f"Quantidade de perguntas: {len(self)}\n"
            f"Pontuação máxima: {self.calcular_pontuacao_maxima()}"
        )
