
class Tema:
    def __init__(self, nome):
        self.nome = nome

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str):
            raise TypeError("O nome do tema deve ser um texto.")

        valor = valor.strip()

        if not valor:
            raise ValueError("O nome do tema não pode estar vazio.")

        self._nome = valor

    def __str__(self):
        return self.nome

    def __eq__(self, outro):
        if not isinstance(outro, Tema):
            return NotImplemented

        return self.nome.casefold() == outro.nome.casefold()
