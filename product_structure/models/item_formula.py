class ItemFormula:
    def __init__(self, nome, descricao="", quantidade=0, preco=0):
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco

    def atualizar_descricao(self, new_desc):
        self.descricao = new_desc

    def atualizar_quantidade(self, new_qtd):
        if new_qtd >= 0:
            self.quantidade = new_qtd

    def atualizar_preco(self, new_price):
        if new_price >= 0:
            self.preco = new_price
