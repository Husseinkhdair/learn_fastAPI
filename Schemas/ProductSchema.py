from pydantic import BaseModel,Field

class ProductSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100,description="The name of the product")
    description: str = Field(..., max_length=255,description="The description of the product")
    price: float = Field(..., gt=0, description="The price of the product")
