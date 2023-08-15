from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid


# FAST API App
app = FastAPI()

# Post Data --> TODO: Store this on a database
posts = []

# Post Model Schema
class Post(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime] = None
    published: bool = False

# Test Fast API
@app.get('/')
def read_root():
    return {"welcome": "welcome to my REST API"}

# Return all posts stored on array posts
@app.get('/posts')
def get_posts():
    return posts

# Store data on array posts
@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.model_dump())
    return "OK!"

# Store post data on array posts with id post_id
@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# Delete post data with post_id
@app.delete("/posts/{post_id}")
def delete_post (post_id: str):
    for index, post in enumerate (posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted successfully", "id": post_id}
    raise HTTPException(status_code=404, detail="Post not found. Cannot be deleted.")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate (posts):
        if post["id"] == post_id:
            posts [index]["title"] = updatedPost.title
            posts [index]["content"] = updatedPost.content
            posts [index]["author"] = updatedPost. author
            return {"message": "Post has been updated successfully", "id": post_id}
    raise HTTPException(status_code=404, detail="Post not found.")
