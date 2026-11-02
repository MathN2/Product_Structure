from dataclasses import dataclass


@dataclass
class NodeDTO:
    node_id: int
    formula_id: int
    item_id: int
    parent_id: int
    quantidade: int
