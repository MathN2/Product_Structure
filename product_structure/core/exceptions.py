# =====================
# EXCEPTIONS DA ARVORE
# =====================
class TreeError(Exception):
    pass


class TreeEmptyError(TreeError):
    pass


class FormulaAlreadyExistsError(TreeError):
    pass


# =====================
#  EXCEPTIONS DO NODE
# =====================
class NodeError(Exception):
    pass


class NodeEmptyError(NodeError):
    pass


class NodeValueError(NodeError):
    pass


class NodeAlreadyExistsError(NodeError):
    pass


# =====================
#  EXCEPTIONS DO ITEM
# =====================
class ItemError(Exception):
    pass


class ItemBeingUsedError(ItemError):
    pass
