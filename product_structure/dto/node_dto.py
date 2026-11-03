from dataclasses import dataclass


@dataclass
class NodeDTO:
    formula_id: int
    item_id: int
    quantidade: int
    parent_id: int | None = None
    node_id: int | None = None
