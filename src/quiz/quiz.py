# Classe Quiz
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
        self.titulo = titulo
        self.perguntas = perguntas if perguntas is not None else []
        self.limite_tempo = limite_tempo
        self.limite_tentativas = limite_tentativas
        self.valor_bonus = valor_bonus
        self.professor = professor

        self.validar()

    # Validação dos dados do Quiz
    def validar(self):

        if not isinstance(self.titulo, str) or self.titulo.strip() == "":
            raise ValueError("O título do Quiz não pode estar vazio.")

        if not isinstance(self.perguntas, list):
            raise TypeError("As perguntas devem estar em uma lista.")

        for pergunta in self.perguntas:
            from pergunta import Pergunta

            if not isinstance(pergunta, Pergunta):
                raise TypeError("O Quiz só pode possuir objetos Pergunta.")

        if self.limite_tempo is not None:
            if not isinstance(self.limite_tempo, (int, float)):
                raise TypeError("O limite de tempo deve ser numérico.")

            if self.limite_tempo <= 0:
                raise ValueError("O limite de tempo deve ser maior que zero.")

        if self.limite_tentativas is not None:
            if not isinstance(self.limite_tentativas, int):
                raise TypeError("O limite de tentativas deve ser inteiro.")

            if self.limite_tentativas <= 0:
                raise ValueError("O limite de tentativas deve ser maior que zero.")

        if not isinstance(self.valor_bonus, (int, float)):
            raise TypeError("O valor do bônus deve ser numérico.")

        if self.valor_bonus < 0:
            raise ValueError("O valor do bônus não pode ser negativo.")

        return True

    # Adiciona uma pergunta ao Quiz
    def adicionar_pergunta(self, pergunta):

        from pergunta import Pergunta

        if not isinstance(pergunta, Pergunta):
            raise TypeError("É necessário adicionar uma Pergunta.")

        for pergunta_existente in self.perguntas:
            if pergunta_existente == pergunta:
                raise ValueError(
                    "Não é possível adicionar uma pergunta duplicada."
                )

        self.perguntas.append(pergunta)

    # Remove uma pergunta do Quiz
    def remover_pergunta(self, pergunta):

        if pergunta not in self.perguntas:
            raise ValueError("A pergunta não está neste Quiz.")

        self.perguntas.remove(pergunta)

    # Altera a ordem das perguntas
    def alterar_ordem_perguntas(self, nova_ordem):

        if not isinstance(nova_ordem, list):
            raise TypeError("A nova ordem deve ser uma lista.")

        if len(nova_ordem) != len(self.perguntas):
            raise ValueError(
                "A nova ordem deve possuir a mesma quantidade de perguntas."
            )

        if set(nova_ordem) != set(self.perguntas):
            raise ValueError(
                "A nova ordem deve conter exatamente as perguntas do Quiz."
            )

        self.perguntas = nova_ordem

    # Calcula a pontuação máxima do Quiz
    def calcular_pontuacao_maxima(self):

        pontuacao = 0

        for pergunta in self.perguntas:
            pontuacao += pergunta.calcular_pontuacao()

        return pontuacao + self.valor_bonus

    # Retorna a quantidade de perguntas
    def __len__(self):

        return len(self.perguntas)

    # Representação do Quiz
    def __str__(self):

        return (
            f"Quiz: {self.titulo}\n"
            f"Quantidade de perguntas: {len(self.perguntas)}\n"
            f"Pontuação máxima: {self.calcular_pontuacao_maxima()}"
        )