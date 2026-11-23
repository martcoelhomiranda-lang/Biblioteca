from model.Usuario import Usuario


class Cliente(Usuario):
    """Cliente: vê só os próprios empréstimos e pode renová-los."""

    def getTipo(self):
        return "Cliente"

    def visualizarEmprestimos(self, biblioteca):
        emprestimos = biblioteca.getEmprestimosDoCliente(self)
        if not emprestimos:
            print("\n   Você não tem empréstimos.")
            return
        for emp in emprestimos:
            print(f"\n{emp}")

    def renovarEmprestimo(self, biblioteca, codigo):
        emp = biblioteca.buscarEmprestimo(codigo)
        # Um cliente só pode renovar empréstimo que é DELE.
        if emp is None or emp.getCliente() is not self:
            raise ValueError(f"empréstimo {codigo} não encontrado para você.")
        emp.renovar()
        biblioteca.salvarEmprestimos()

    def exibirMenu(self, biblioteca):
        while True:
            print(f"\n=== Menu do Cliente — {self.getNome()} ===")
            print("1 - Ver meus empréstimos")
            print("2 - Renovar um empréstimo")
            print("0 - Sair")
            opcao = input("Escolha: ").strip()
            if opcao == "1":
                self.visualizarEmprestimos(biblioteca)
            elif opcao == "2":
                try:
                    self.renovarEmprestimo(biblioteca, int(input("Código do empréstimo: ")))
                    print("   Empréstimo renovado!")
                except ValueError as erro:
                    print(f"   Não foi possível renovar: {erro}")
            elif opcao == "0":
                break
            else:
                print("   Opção inválida.")
