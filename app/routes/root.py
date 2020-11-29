import re
from fastapi import File, UploadFile, Body, HTTPException
from fastapi.routing import APIRouter


root = APIRouter()


@root.post('/getMatch')
def getMatch(
    image: UploadFile = File(...),
    links: list[str] = Body(..., regex=r'^(?:id\d+|\w+)$')
):
    if not image.content_type.startswith('image/'):
        raise HTTPException(415, 'Bad image mime type')

    raise HTTPException(501)
