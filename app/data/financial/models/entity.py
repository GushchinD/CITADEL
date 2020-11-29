from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class EntityStatus(str, Enum):
    active = 'active'
    liquidated = 'liquidated'


@dataclass
class Entity:
    type = 'Entity'
    name: str
    itn: str
    owner_itn: Optional[str] = None
    status: Optional[EntityStatus] = None
