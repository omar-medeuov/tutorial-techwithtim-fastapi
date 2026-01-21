from fastapi import FastAPI

app = FastAPI()

text_posts = {1 : {"title": "New Post", "content": "Cool test post"}}

@app.get("/posts")
def get_all_posts():
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    return text_posts.get(id)



#22:02 CRUD

# this is how you make an endpoint below (or a path)

# @app.get("/hello-world")
# def hello_world():
#     return {"message": "Hello World"}  # ofc returns JSON formatted information

