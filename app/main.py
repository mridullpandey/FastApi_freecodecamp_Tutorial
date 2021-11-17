from typing import Optional
from typing_extensions import runtime
from fastapi import FastAPI,Response,HTTPException,status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
 
app = FastAPI()

my_posts=[{'title':'this is the first post','content':'this is the content for the first post ','id':11},{'title':'this is the second post','content':'this is the content for the post 2','id':4}]

class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]=None
    
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post: post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {'data':post_dict }

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

#function to find index of a post in myposts
def index(id: int):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i


##routing order: always try to have string routes first to have proper route mapping
# routes work top to down 

# @app.get("/posts/latest")
# def get_latest():
#     post=my_posts[len(my_posts)-1]
#     return{'details':post}

@app.get("/posts/{id}")
def get_post(id:int):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")

    return{'post': post}
    
@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #get index of the post in our database
    #my_posts.pop(index)
    i=index(id)
    if i == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    my_posts.pop(i)
    return{'message': 'deleted successfully'}

@app.put('/posts/{id}')
def update_post(id:int,post:post):
    i=index(id)
    if i == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    my_posts.pop(i)
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[i]=post_dict
    return {'data':post_dict}
