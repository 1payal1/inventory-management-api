# from pydantic import BaseModel
# from typing import Optional


# class ItemBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     quantity: int = 0
#     price: float


from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    quantity: int = Field(0, ge=0)
    price: float = Field(..., gt=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("name cannot be blank or just whitespace")
        return v.strip()

class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True