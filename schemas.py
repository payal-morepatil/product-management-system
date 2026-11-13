from pydantic import BaseModel, Field, ConfigDict


# Schema for creating a product
class ProductCreate(BaseModel):

    name: str = Field(min_length=2)
    description: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    category: str


# Schema for returning product details
class ProductResponse(ProductCreate):

    id: int
    model_config = ConfigDict(from_attributes=True)