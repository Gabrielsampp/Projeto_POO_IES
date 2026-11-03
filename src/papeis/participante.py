class Participante:
    def __init__(self):
        self._tentativas = []

    @property
    def tentativas(self):
        return tuple(self._tentativas)

    def adicionar_tentativa(self, tentativa):
        from src.tentativa.tentativa import Tentativa

        if not isinstance(tentativa, Tentativa):
            raise TypeError("É necessário fornecer uma Tentativa.")

        if tentativa.participante is not self:
            raise ValueError("A tentativa pertence a outro participante.")

        if tentativa in self._tentativas:
            raise ValueError("Essa tentativa já foi registrada.")

        self._tentativas.append(tentativa)
