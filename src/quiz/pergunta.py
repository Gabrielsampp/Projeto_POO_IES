# Classe Pergunta
class Pergunta:

    def __init__(self, tema, enunciado, alternativas, indice_correto, dificuldade):

        self.tema = tema
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.indice_correto = indice_correto
        self.dificuldade = dificuldade

        self.validar()

    # Validação dos dados da pergunta
    def validar(self):

        # Validação do tema
        if self.tema is None or str(self.tema).strip() == "":
            raise ValueError("O tema não pode estar vazio.")

        # Validação do enunciado
        if self.enunciado is None or str(self.enunciado).strip() == "":
            raise ValueError("O enunciado não pode estar vazio.")

        # Validação da quantidade de alternativas
        if not isinstance(self.alternativas, list):
            raise TypeError("As alternativas devem estar em uma lista.")

        if len(self.alternativas) < 3 or len(self.alternativas) > 5:
            raise ValueError("A pergunta deve possuir entre 3 e 5 alternativas.")

        # Validação das alternativas
        for alternativa in self.alternativas:
            if not isinstance(alternativa, str) or alternativa.strip() == "":
                raise ValueError("As alternativas não podem estar vazias.")

        # Validação de alternativas duplicadas
        alternativas_limpo = []

        for alternativa in self.alternativas:
            alternativa = alternativa.strip().lower()

            if alternativa in alternativas_limpo:
                raise ValueError("Não podem existir alternativas duplicadas.")

            alternativas_limpo.append(alternativa)

        # Validação do índice correto
        if not isinstance(self.indice_correto, int):
            raise TypeError("O índice correto deve ser um número inteiro.")

        if self.indice_correto < 0 or self.indice_correto >= len(self.alternativas):
            raise ValueError("O índice correto não corresponde a uma alternativa válida.")

        # Validação da dificuldade
        if self.dificuldade not in ["F", "M", "D"]:
            raise ValueError("A dificuldade deve ser F, M ou D.")

        return True

    # Adiciona uma alternativa
    def adicionar_alternativa(self, alternativa):

        if not isinstance(alternativa, str) or alternativa.strip() == "":
            raise ValueError("A alternativa não pode estar vazia.")

        if len(self.alternativas) >= 5:
            raise ValueError("A pergunta não pode possuir mais de 5 alternativas.")

        for existente in self.alternativas:
            if existente.strip().lower() == alternativa.strip().lower():
                raise ValueError("A alternativa já existe.")

        self.alternativas.append(alternativa.strip())

    # Remove uma alternativa
    def remover_alternativa(self, indice):

        if len(self.alternativas) <= 3:
            raise ValueError("A pergunta deve possuir pelo menos 3 alternativas.")

        if indice < 0 or indice >= len(self.alternativas):
            raise IndexError("Índice de alternativa inválido.")

        if indice == self.indice_correto:
            raise ValueError("Não é possível remover a alternativa correta.")

        self.alternativas.pop(indice)

        # Ajusta o índice correto caso uma alternativa anterior tenha sido removida
        if indice < self.indice_correto:
            self.indice_correto -= 1

    # Altera uma alternativa
    def alterar_alternativa(self, indice, alternativa):

        if indice < 0 or indice >= len(self.alternativas):
            raise IndexError("Índice de alternativa inválido.")

        if not isinstance(alternativa, str) or alternativa.strip() == "":
            raise ValueError("A alternativa não pode estar vazia.")

        for i, existente in enumerate(self.alternativas):

            if i != indice and existente.strip().lower() == alternativa.strip().lower():
                raise ValueError("A alternativa já existe.")

        self.alternativas[indice] = alternativa.strip()

    # Verifica se uma resposta está correta
    def verificar_resposta(self, indice):

        return indice == self.indice_correto

    # Calcula a pontuação da pergunta
    def calcular_pontuacao(self):

        if self.dificuldade == "F":
            return 1

        elif self.dificuldade == "M":
            return 2

        elif self.dificuldade == "D":
            return 3

        return 0

    # Representação da pergunta
    def __str__(self):

        return (
            f"Tema: {self.tema}\n"
            f"Enunciado: {self.enunciado}\n"
            f"Alternativas: {self.alternativas}\n"
            f"Índice correto: {self.indice_correto}\n"
            f"Dificuldade: {self.dificuldade}"
        )

    # Compara duas perguntas
    def __eq__(self, outra_pergunta):

        if not isinstance(outra_pergunta, Pergunta):
            return False

        return (
            self.enunciado == outra_pergunta.enunciado
            and self.tema == outra_pergunta.tema
        )