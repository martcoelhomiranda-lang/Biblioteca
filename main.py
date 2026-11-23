import os

from model.Biblioteca import Biblioteca


def principal():
    # pasta do main.py: os .txt ficam junto dele
    pasta = os.path.dirname(os.path.abspath(__file__))
    biblioteca = Biblioteca(pasta)
    biblioteca.carregarDados()

    login = input("\nLogin: ").strip()
    senha = input("Senha: ").strip()

    usuario = biblioteca.autenticar(login, senha)
    if usuario is None:
        print("Acesso negado.")
        return

    print(f"\nBem-vindo(a), {usuario.getNome()}!")
    # Polimorfismo: a mesma mensagem, comportamento diferente por tipo de usuário.
    usuario.exibirMenu(biblioteca)


if __name__ == '__main__':
    principal()
