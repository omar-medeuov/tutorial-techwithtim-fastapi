from pydantic import BaseModel

# inherit from base model, use this class as a type to
# receive body data inside our functions (app.py)

class PostCreate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    title: str
    content: str

