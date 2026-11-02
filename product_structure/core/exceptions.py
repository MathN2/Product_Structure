# =====================
# EXCEPTIONS DA ARVORE
# =====================
class TreeError(Exception):
    pass

class TreeEmptyError(TreeError):
    pass


# =====================
#  EXCEPTIONS DO NODE
# =====================
class NodeError(Exception):
    pass

class NodeEmptyError(NodeError):
    pass


# =====================
#  EXCEPTIONS DO ITEM
# =====================
class ItemError(Exception):
    pass

class ItemBeingUsedError(ItemError):
    pass