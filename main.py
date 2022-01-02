from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True


my_posts = [
    {
        "title": "My first post",
        "content": "Here you are gonin to find a specific post",
        "rating": None,
        "published": True,
        "id": 1,
    },
    {
        "title": "Second post",
        "content": "Just another post",
        "rating": 3,
        "published": False,
        "id": 2,
    },
]


@app.get("/")
def read_root():
    data = {
        "message": "Hello world!",
        "info": "It's working!",
    }
    return data


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    data = find_post(id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post whit id: {id} not found",
        )
    return {"post": data}


@app.get("/posts")
def get_posts():
    data = my_posts
    return {"posts": data}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(data: Post):
    post_dict = data.dict()
    post_dict["id"] = randrange(0, 10000000000)
    my_posts.append(post_dict)
    new_post = post_dict
    return {"new_post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    data = find_index_post(id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post whit id: {id} not found",
        )
    my_posts.pop(data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    current_data = find_index_post(id)
    if current_data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post whit id: {id} not found",
        )
    updated_data = post.dict()
    updated_data["id"] = id
    my_posts[current_data] = updated_data
    print(post)
    return {"updated_post": updated_data}
