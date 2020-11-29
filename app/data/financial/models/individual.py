from typing import Optional
from dataclasses import dataclass
from .entity import EntityStatus


@dataclass
class Individual:
    type = 'Individual'
    name: str
    itn: str
    status: Optional[EntityStatus] = None
