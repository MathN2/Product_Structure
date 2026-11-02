from product_structure.core.exceptions import *
from product_structure.core.node import Node


class ArvoreFormula:
    def __init__(self):
        self.root: Node | None = None
        self.nodes: dict[int, Node] = {}

    def get_nodes(self):
        return self.nodes.values()

    def inserir(self, node, parent=None):
        if node is None:
            raise NodeEmptyError("Node não pode ser None.")

        if parent is None:
            self.root = node
            self.nodes[node.node_id] = node
            return node

        if parent.node_id in self.nodes:
            parent.children.append(node)
            node.parent = parent
            self.nodes[node.node_id] = node
            return node

        else:
            print("Pai inexistente.")

        return None

    def remover(self, node: Node):
        if node is None:
            raise NodeEmptyError("Node não pode ser None.")

        if node.node_id in self.nodes:
            if not node.parent is None:
                node.parent.children.remove(node)

            self.nodes.pop(node.node_id)

            for n in node.children:
                self.remover(n)

    def alterar(self, node, new_value):
        if node is None:
            raise NodeEmptyError("Node não pode ser None.")

        if node.node_id in self.nodes:
            self.nodes[node.node_id].value = new_value

    def buscar_por_id(self, search_id: int) -> Node | None:
        return self.nodes.get(search_id)

    def buscar_por_nome(self, name: str) -> dict[int, Node]:
        resultado = {}

        for node in self.nodes.values():
            if node.value.nome == name:
                resultado[node.node_id] = node

        return resultado

    def implosao(self):
        if not self.nodes:
            return

        resultado = 0
        for node in self.nodes.values():
            if node.parent is None:
                continue

            resultado += node.value.preco

        return resultado

    def explosao(self):
        pass
