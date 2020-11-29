from typing import List
from fastapi import File, UploadFile, Body, HTTPException
from fastapi.routing import APIRouter
from re import match
from pydantic import HttpUrl
from app.data.financial.collect_data import collect_data

root = APIRouter()


def check_link(link: HttpUrl):
    return (
            link.host == 'vk.com' and
            link.scheme == 'https' and
            link.user is None and link.password is None and
            link.port is None and
            match(r'^/(?:id\d+|[\w\.]+)$', link.path) is not None and
            link.query is None and link.fragment is None
    )


@root.post('/getMatch')
async def get_match(
        image: UploadFile = File(...),
        links: List[HttpUrl] = Body(...)
):
    if not image.content_type.startswith('image/'):
        print('Bad image mime type', image.content_type)
        raise HTTPException(415, 'Bad image mime type')
    if not all(map(check_link, links)):
        print('URLs must be vk profile links', links)
        raise HTTPException(406, 'URLs must be vk profile links')
    words, trust, first, last, itns, arbits = collect_data(await image.read(), links)
    words = words.to_dict()
    trust = float(trust)
    # print(words)
    return {
        'words': words,
        'trust': trust,
        'name': f'{first} {last}',
        'itns': itns,
        'arbits': arbits
    }
