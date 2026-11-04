from pydantic import BaseModel


class NodeCreate(BaseModel):
    item_id: int
    quantidade: float
    parent_id: int | None = None