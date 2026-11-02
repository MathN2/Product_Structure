class ItemFormula:
    def __init__(self, nome, descricao="", preco=0.0):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    def atualizar_descricao(self, new_desc):
        self.descricao = new_desc

    def atualizar_preco(self, new_price):
        if new_price >= 0:
            self.preco = new_price
