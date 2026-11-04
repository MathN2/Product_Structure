from pydantic import BaseModel


class NodeCreate(BaseModel):
    item_id: int
    quantidade: int
    parent_id: int | None = None