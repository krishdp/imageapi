from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from .. database import get_db
from .. import models, schemas, oauth2
import random
import string
import shutil
from starlette.responses import Response
from PIL import Image
from typing import List


router = APIRouter(
    prefix='/posts',
    tags=['Post']
)

image_url_types = ['absolute', 'relative']

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.post('/', response_model=PostDisplay )
# def create(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     if not request.image_url_type in image_url_types:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                             detail="Parameter image_url_type can only take values 'absolute' or 'relatives'.")
#     return db_post.create(db, request)


@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


@router.get('/{id}', response_model=schemas.Post)
def get_posts_id(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")

    # if pos t.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized for perform action")

    return post


@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: int = Depends(oauth2.get_current_user)):
    print("1",image.filename)
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    print("2",filename)
    path = f'app/images/{filename}'

    if not (filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.gif') or filename.endswith('.tiff')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Filename is not a image file")

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}


@router.post('/resize')
def resize(image:str, height:int, width:int, current_user: int = Depends(oauth2.get_current_user)):
    name = f"app/images/{image}"
    im = Image.open(name)
    width, height = im.size
    left = 6
    top = height / 4
    right = 174
    bottom = 3 * height / 4
    
    newsize =(height, width)
    im1 = im.crop((left, top, right, bottom))
    im1 = im1.resize(newsize)
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.rsplit('.', 1))
    im1.save(f"app/resizeimages/{filename}")
    im1.show()
    path = f'app/resizeimages/{filename}'
    return path


@router.delete('/{id}',response_model=schemas.Post)
def delete(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = post = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized for perform action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform this action")
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    
    return post_query.first()
