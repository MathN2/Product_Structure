from dataclasses import dataclass, field


@dataclass
class Node[T]:
    value: T
    node_id: int | None = None
    formula_id: int | None = None
    parent_id: int | None = None
    children: list[Node[T]] = field(default_factory=list)
    quantidade: int = 1
