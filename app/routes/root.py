from fastapi import File, UploadFile, Body, HTTPException
from fastapi.routing import APIRouter
from pydantic import HttpUrl, stricturl

from re import match

root = APIRouter()

def check_link(link: HttpUrl):
    return (
        link.host == 'vk.com' and
        link.scheme == 'https' and
        link.user is None and link.password is None and
        link.port is None and
        match(r'^/(?:id\d+|\w+)$', link.path) is not None and
        link.query is None and link.fragment is None
    )


@root.post('/getMatch')
def getMatch(
    image: UploadFile = File(...),
    links: list[HttpUrl] = Body(...)
):
    if not image.content_type.startswith('image/'):
        raise HTTPException(415, 'Bad image mime type')
    if not all(map(check_link, links)):
        raise HTTPException(406, 'URLs must be vk profile links')

    raise HTTPException(501)
