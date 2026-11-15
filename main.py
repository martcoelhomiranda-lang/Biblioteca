import os

from model.Biblioteca import Biblioteca


def principal():
    # pasta do main.py: os .txt ficam junto dele
    pasta = os.path.dirname(os.path.abspath(__file__))
    biblioteca = Biblioteca(pasta)
    biblioteca.carregarDados()

    # TODO (front): pedir login e senha e chamar biblioteca.autenticar(login, senha)
    # TODO (front): se None -> "Acesso negado"; senão -> usuario.exibirMenu(biblioteca)


if __name__ == '__main__':
    principal()