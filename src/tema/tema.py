class Tema:
    def __init__(self, nome):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome do tema não pode estar vazio.")

        self.nome = nome.strip()

    def __str__(self):
        return self.nome

    def __eq__(self, outro):
        if not isinstance(outro, Tema):
            return False

        return self.nome.casefold() == outro.nome.casefold()
