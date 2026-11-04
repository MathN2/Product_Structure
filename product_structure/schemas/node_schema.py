from pydantic import BaseModel, Field


class NodeCreate(BaseModel):
    item_id: int
    quantidade: int = Field(ge=1)
    parent_id: int | None = None


class NodeUpdate(BaseModel):
    quantidade: int = Field(ge=1)
