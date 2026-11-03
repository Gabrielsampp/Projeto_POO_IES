
from abc import ABC, abstractmethod


class Usuario(ABC):
    def __init__(self, nome, email, identificador):
        self.nome = nome
        self.email = email
        self.identificador = identificador

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome não pode estar vazio.")

        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str):
            raise TypeError("O e-mail deve ser um texto.")

        valor = valor.strip()

        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError("Informe um e-mail válido.")

        self._email = valor

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O identificador não pode estar vazio.")

        self._identificador = valor.strip()

    @property
    @abstractmethod
    def tipo(self):
        pass

    def __str__(self):
        return (
            f"Nome: {self.nome}\n"
            f"E-mail: {self.email}\n"
            f"Identificador: {self.identificador}\n"
            f"Tipo: {self.tipo}"
        )

    def __eq__(self, outro):
        if not isinstance(outro, Usuario):
            return NotImplemented

        return self.identificador == outro.identificador
