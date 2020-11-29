from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class EntityStatus(str, Enum):
    active = auto()
    liquidated = auto()


@dataclass
class Entity:
    type = 'Entity'
    name: str
    itn: str
    owner_itn: Optional[str] = None
    status: Optional[EntityStatus] = None
