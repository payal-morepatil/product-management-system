from pydantic import BaseModel, Field, ConfigDict

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# create product 
class ProductCreate(BaseModel):
    name : str =Field(min_length=2)
    description : str
    price : float = Field(gt=0)
    quantity :int = Field(ge=0)
    category : str


class ProductResponse(ProductCreate):
    id :int
    model_config = ConfigDict(from_attributes=True)



