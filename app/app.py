from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile

# 1hr the workflow of the controllers is going to be processing the files
# through the backend for security (not directly from FE to imagekit)
# files are going to be stored temporaly and later deleted.


#1hr:13 Imagekit handles image hosting, as well as operations on them

# 58:00 responsible for database creation ??
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

# passing lifespan in as an argument, will run the async function on startup

app = FastAPI(lifespan=lifespan)

# session parameter uses Dependency Injection, happens automatically
# assynchronous session is our dependency
@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # the following variable definition is the core:
        # open the file, upload to imagekit, return metadata that is needed.

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )
        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Make sure to clean up the temporary file with that block
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()
    # Steps: 1. create a new post, 2. add to the session, 3. commit the session (gets added to the db)
    post = Post(
        caption=caption,
        url="dummyurl",
        file_type="photo",
        file_name="Dummy name"
    )
    session.add(post)
    await session.commit()

    # the following line has to do with the fields, values for which are auto created.
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feed(
        session: AsyncSession = Depends(get_async_session)
):
    # querying below, very similar to django queries, also inside views
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
            }
        )
    return posts_data

# 1hr Commenting out the pre-db structure:
#
# # Right, So at this early stage this dictionary is basically our DB
# # The methods read the values from here to return to the user
# # the post method writes the newly created values to this dictionary
#
# text_posts = {
#     1: {"title": "New Post", "content": "Cool test post"},
#     2: {"title": "FastAPI Basics", "content": "Learning how to build APIs with FastAPI"},
#     3: {"title": "Python Tips", "content": "Dictionaries are incredibly useful data structures"},
#     4: {"title": "REST API Design", "content": "Keep your endpoints simple and predictable"},
#     5: {"title": "JSON Explained", "content": "JSON maps naturally to Python dictionaries"},
#     6: {"title": "Weekend Project", "content": "Building a simple e-commerce backend"},
# }
#
# # Adding limit parameter with the idea of receiving part of the posts
# # limit function parameter acts as a query parameter later
# # type hints help the framework (Pydantic) automatically documented and validated
# # I noticed getting validation errors in Swagger when trying to send a request with a different type.
#
# @app.get("/posts")
# def get_all_posts(limit: int = None):
#     if limit:
#         return list(text_posts.values())[:limit]
#
#     return text_posts
#
#
# # without a type hint for id parameter, can't get the values
# @app.get("/posts/{id}")
# def get_post(id:int) -> PostResponse:
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found")
#
#     return text_posts.get(id)
#
# # request body. it's hidden, schema has to be used.
# # So by using a schema class as the type for the parameter
# # we let fastapi know that we should be receiving a request body
# # and not a query parameter!
# @app.post("/posts")
# def create_post(post: PostCreate) -> PostResponse:
#     new_post = {"title": post.title, "content": post.content}
#     # Because the attributes of PostCreate have type hints, Pydantic will add a check?
#     text_posts[max(text_posts.keys()) +1] = {"title": post.title, "content": post.content}
#     # return new_post
#     return new_post
#
#
#
#
# # 44:00 without return types, the swagger doc is not going to be very informative.
#
#
# #22:02 CRUD
#
# # this is how you make an endpoint below (or a path)
#
# # @app.get("/hello-world")
# # def hello_world():
# #     return {"message": "Hello World"}  # ofc returns JSON formatted information
#
