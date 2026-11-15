from datetime import date, datetime, timedelta

class Emprestimo:
    """Empréstimo de 1 a 3 livros feitos por um cliente."""

    PRAZO_DIAS = 14
    MAX_RENOVACOES = 2
    MULTA_POR_DIA = 1.50
    MAX_LIVROS = 3
    FORMATO_DATA = "%d/%m/%Y"


    def __init__(self, codigo, cliente, dataEmprestimo, renovacoes=0):
        self.__codigo = codigo
        self.__cliente = cliente
        self.__dataEmprestimo = dataEmprestimo
        self.__renovacoes = renovacoes
        self.__livros = []

    def getCodigo(self):
        return self.__codigo

    def setCodigo(self, codigo):
        self.__codigo = codigo

    def getCliente(self):
        return self.__cliente

    def setCliente(self, cliente):
        self.__cliente = cliente

    def getDataEmprestimo(self):
        return self.__dataEmprestimo

    def setDataEmprestimo(self, dataEmprestimo):
        self.__dataEmprestimo = dataEmprestimo

    def getRenovacoes(self):
        return self.__renovacoes

    def setRenovacoes(self, renovacoes):
        self.__renovacoes = renovacoes

    def getLivros(self):
        return self.__livros

    def addLivro(self, livro):
        if len(self.__livros) >= Emprestimo.MAX_LIVROS:
            raise ValueError(f"empréstimo {self.__codigo} já tem {Emprestimo.MAX_LIVROS} livros")
        self.__livros.append(livro)

    def removeLivro(self, livro):
        if livro in self.__livros:
            self.__livros.remove(livro)

    def getDataDevolucao(self):
        """Data do empréstimo + 14 dias, mais 14 dias por renovação."""
        dias = Emprestimo.PRAZO_DIAS * (1 + self.__renovacoes)
        return self.__dataEmprestimo + timedelta(days=dias)

    def getDiasAtraso(self):
        atraso = (date.today() - self.getDataDevolucao()).days
        return max(0, atraso)

    def estaAtrasado(self):
        return self.getDiasAtraso() > 0

    def calcularMulta(self):
        """R$ 1,50 por dia de atraso, por livro."""
        return self.getDiasAtraso() * Emprestimo.MULTA_POR_DIA * len(self.__livros)

    def renovar(self):
        """Renova se as regras permitirem; senão lança ValueError com o motivo."""
        if self.estaAtrasado():
            raise ValueError(f"Empréstimo {self.__codigo} está atrasado e não pode ser renovado.")
        if self.__renovacoes >= Emprestimo.MAX_RENOVACOES:
            raise ValueError(f"Empréstimo {self.__codigo} já atingiu o limite de renovações.")
        self.__renovacoes += 1

    @staticmethod
    def converterData(texto):
        """Converte 'dd/mm/aaaa' em date; lança ValueError se for inválida."""
        try:
            return datetime.strptime(texto.strip(), Emprestimo.FORMATO_DATA).date()
        except ValueError:
            raise ValueError(f"data inválida '{texto}' (use dd/mm/aaaa)")

    @staticmethod
    def formatarData(data):
        return data.strftime(Emprestimo.FORMATO_DATA)

    @staticmethod
    def formatarMoeda(valor):
        return f"R$ {valor:.2f}".replace(".", ",")

    def __str__(self):
        texto = (f"Empréstimo nº {self.__codigo} | Cliente: {self.__cliente.getNome()}\n"
                 f"   Emprestado em: {self.formatarData(self.__dataEmprestimo)}"
                 f" | Devolução: {self.formatarData(self.getDataDevolucao())}"
                 f" | Renovações: {self.__renovacoes}/{Emprestimo.MAX_RENOVACOES}\n"
                 f"   Livros:\n")
        for livro in self.__livros:
            texto += f"      {livro}\n"
        if self.estaAtrasado():
            texto += (f"   ATRASADO há {self.getDiasAtraso()} dia(s) → "
                      f"Multa: {self.formatarMoeda(self.calcularMulta())}")
        else:
            texto += "   Em dia (sem multa)"
        return texto