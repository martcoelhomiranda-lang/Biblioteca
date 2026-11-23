from abc import ABC, abstractmethod


class Usuario(ABC):
    """Classe abstrata: base para Cliente e Bibliotecario."""

    def __init__(self, codigo, nome, login, senha):
        self.__codigo = codigo
        self.__nome = nome
        self.__login = login
        self.__senha = senha

    # O código é a IDENTIDADE do objeto: não tem setter (ver explicação).
    def getCodigo(self):
        return self.__codigo

    def getNome(self):
        return self.__nome

    def setNome(self, nome):
        self.__nome = nome

    def getLogin(self):
        return self.__login

    # A senha só pode ser trocada ou conferida, nunca lida de fora.
    def setSenha(self, senha):
        self.__senha = senha

    def validarAcesso(self, login, senha):
        """Retorna True se login e senha conferem."""
        return self.__login == login and self.__senha == senha

    @abstractmethod
    def getTipo(self):
        pass

    @abstractmethod
    def exibirMenu(self, biblioteca):
        pass

    @abstractmethod
    def visualizarEmprestimos(self, biblioteca):
        pass

    def __str__(self):
        return f"{self.getTipo()}: {self.__nome} (código {self.__codigo})"
