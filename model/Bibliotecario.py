from model.Usuario import Usuario


class Bibliotecario(Usuario):
    """Bibliotecário: vê os empréstimos de todos e não renova."""

    def getTipo(self):
        return "Bibliotecario"

    def visualizarEmprestimos(self, biblioteca):
        emprestimos = biblioteca.getEmprestimos()
        if not emprestimos:
            print("\n   Nenhum empréstimo cadastrado.")
            return
        for emp in emprestimos:
            print(f"\n{emp}")

    def exibirMenu(self, biblioteca):
        while True:
            print(f"\n=== Menu do Bibliotecário — {self.getNome()} ===")
            print("1 - Ver todos os empréstimos")
            print("0 - Sair")
            opcao = input("Escolha: ").strip()
            if opcao == "1":
                self.visualizarEmprestimos(biblioteca)
            elif opcao == "0":
                break
            else:
                print("   Opção inválida.")
