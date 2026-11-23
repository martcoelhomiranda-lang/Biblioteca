import os
from model.Cliente import Cliente
from model.Bibliotecario import Bibliotecario
from model.Livro import Livro
from model.Emprestimo import Emprestimo


class Biblioteca:
    """Classe central: guarda acervo, usuários e empréstimos e lê/grava os .txt."""

    SEPARADOR = ";"

    def __init__(self, pasta):
        self.__pasta = pasta
        self.__usuarios = {}
        self.__livros = []
        self.__emprestimos = {}

    def getUsuarios(self):
        return list(self.__usuarios.values())

    def getLivros(self):
        return list(self.__livros)  # cópia: não expõe a lista interna

    def getEmprestimos(self):
        return list(self.__emprestimos.values())

    def addUsuario(self, usuario):
        if usuario.getCodigo() in self.__usuarios:
            raise ValueError(f"código de usuário {usuario.getCodigo()} duplicado")
        self.__usuarios[usuario.getCodigo()] = usuario

    def removeUsuario(self, usuario):
        self.__usuarios.pop(usuario.getCodigo(), None)

    def addLivro(self, livro):
        if self.buscarLivro(livro.getCodigo()) is not None:
            raise ValueError(f"código de livro {livro.getCodigo()} duplicado")
        self.__livros.append(livro)

    def removeLivro(self, livro):
        if livro in self.__livros:
            self.__livros.remove(livro)

    def addEmprestimo(self, emprestimo):
        self.__emprestimos[emprestimo.getCodigo()] = emprestimo

    def removeEmprestimo(self, emprestimo):
        self.__emprestimos.pop(emprestimo.getCodigo(), None)

    def buscarLivro(self, codigo):
        for livro in self.__livros:
            if livro.getCodigo() == codigo:
                return livro
        return None

    def buscarEmprestimo(self, codigo):
        return self.__emprestimos.get(codigo)

    def livroEmprestado(self, livro):
        """True se o livro já está em algum empréstimo (não está disponível)."""
        return any(livro in e.getLivros() for e in self.__emprestimos.values())

    def getEmprestimosDoCliente(self, cliente):
        """Só os empréstimos do cliente informado."""
        return [e for e in self.__emprestimos.values() if e.getCliente() is cliente]

    def autenticar(self, login, senha):
        """Retorna o usuário se login/senha conferirem; senão None."""
        for usuario in self.__usuarios.values():
            if usuario.validarAcesso(login, senha):
                return usuario
        return None

    def __caminho(self, nomeArquivo):
        return os.path.join(self.__pasta, nomeArquivo)

    def __lerArquivo(self, nomeArquivo):
        """Lê um .txt e devolve uma lista de (número da linha, lista de campos)."""
        linhas = []
        try:
            with open(self.__caminho(nomeArquivo), "r", encoding="utf-8") as arquivo:
                for numero, linha in enumerate(arquivo, start=1):
                    linha = linha.strip()
                    if linha:  # ignora linhas em branco
                        campos = [campo.strip() for campo in linha.split(self.SEPARADOR)]
                        linhas.append((numero, campos))
        except FileNotFoundError:
            print(f"   ERRO: arquivo '{nomeArquivo}' não encontrado.")
            return linhas
        print(f"   {nomeArquivo}: {len(linhas)} linha(s) lida(s)")
        return linhas

    def __avisoLinha(self, nomeArquivo, numero, erro):
        print(f"   AVISO: {nomeArquivo}, linha {numero} ignorada: {erro}")

    def __carregarUsuarios(self):
        # dicionário que liga o tipo escrito no arquivo à classe correspondente
        tipos = {"Cliente": Cliente, "Bibliotecario": Bibliotecario}
        for numero, campos in self.__lerArquivo("usuarios.txt"):
            try:
                codigo, nome, tipo, login, senha = campos
                if tipo not in tipos:
                    raise ValueError(f"tipo de usuário desconhecido '{tipo}'")
                self.addUsuario(tipos[tipo](int(codigo), nome, login, senha))
            except ValueError as erro:
                self.__avisoLinha("usuarios.txt", numero, erro)

    def __carregarLivros(self):
        for numero, campos in self.__lerArquivo("livros.txt"):
            try:
                codigo, titulo, autor = campos
                self.addLivro(Livro(int(codigo), titulo, autor))
            except ValueError as erro:
                self.__avisoLinha("livros.txt", numero, erro)

    def __carregarEmprestimos(self):
        """Cada linha tem 1 livro; linhas com o mesmo código viram UM Emprestimo."""
        for numero, campos in self.__lerArquivo("emprestimos.txt"):
            try:
                if len(campos) not in (4, 5):
                    raise ValueError(f"esperados 4 ou 5 campos, encontrados {len(campos)}")
                codigo = int(campos[0])
                codCliente = int(campos[1])
                codLivro = int(campos[2])
                data = Emprestimo.converterData(campos[3])
                renovacoes = int(campos[4]) if len(campos) == 5 else 0

                cliente = self.__usuarios.get(codCliente)
                if not isinstance(cliente, Cliente):
                    raise ValueError(f"cliente {codCliente} não existe")
                livro = self.buscarLivro(codLivro)
                if livro is None:
                    raise ValueError(f"livro {codLivro} não existe")

                if self.livroEmprestado(livro):
                    raise ValueError(f"livro {codLivro} já está emprestado")

                # 1ª linha desse código: cria o empréstimo; nas demais, só adiciona o livro
                emprestimo = self.__emprestimos.get(codigo)
                if emprestimo is None:
                    emprestimo = Emprestimo(codigo, cliente, data, renovacoes)
                emprestimo.addLivro(livro)  # se falhar, nada foi registrado
                self.__emprestimos[codigo] = emprestimo
            except ValueError as erro:
                self.__avisoLinha("emprestimos.txt", numero, erro)

    def carregarDados(self):
        print("\n   Carregando dados...")
        self.__carregarUsuarios()
        self.__carregarLivros()
        self.__carregarEmprestimos()  # precisa de usuários e livros já carregados

    def salvarEmprestimos(self):
        """Regrava o emprestimos.txt (uma linha por livro) com o nº de renovações."""
        try:
            with open(self.__caminho("emprestimos.txt"), "w", encoding="utf-8") as arquivo:
                for emp in self.__emprestimos.values():
                    for livro in emp.getLivros():
                        campos = [emp.getCodigo(), emp.getCliente().getCodigo(),
                                  livro.getCodigo(),
                                  Emprestimo.formatarData(emp.getDataEmprestimo()),
                                  emp.getRenovacoes()]
                        arquivo.write(self.SEPARADOR.join(str(c) for c in campos) + "\n")
        except OSError as erro:
            print(f"   ERRO ao gravar emprestimos.txt: {erro}")
