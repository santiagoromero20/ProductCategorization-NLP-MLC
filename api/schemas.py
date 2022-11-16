from pydantic import BaseModel

#Feedback
class ProductCreate(BaseModel):
    title: str
    description: str
    prediction: str

class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    prediction: str

    class Config:
        orm_mode = True