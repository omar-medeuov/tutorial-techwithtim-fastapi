from fastapi import FastAPI, HTTPException

app = FastAPI()

text_posts = {
    1: {"title": "New Post", "content": "Cool test post"},
    2: {"title": "FastAPI Basics", "content": "Learning how to build APIs with FastAPI"},
    3: {"title": "Python Tips", "content": "Dictionaries are incredibly useful data structures"},
    4: {"title": "REST API Design", "content": "Keep your endpoints simple and predictable"},
    5: {"title": "JSON Explained", "content": "JSON maps naturally to Python dictionaries"},
    6: {"title": "Weekend Project", "content": "Building a simple e-commerce backend"},
}

# Adding limit parameter with the idea of receiving part of the posts
# limit function parameter acts as a query parameter later
# type hints help the framework (Pydantic) automatically documented and validated
# I noticed getting validation errors in Swagger when trying to send a request with a different type.

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]

    return text_posts


# without a type hint for id parameter, can't get the values
@app.get("/posts/{id}")
def get_post(id:int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")

    return text_posts.get(id)



#22:02 CRUD

# this is how you make an endpoint below (or a path)

# @app.get("/hello-world")
# def hello_world():
#     return {"message": "Hello World"}  # ofc returns JSON formatted information

