from pydantic import BaseModel


class Entity(BaseModel):
    _type_id: str


class Light(Entity):
    """Light configuration"""
    _type_id: str = "light"
    name: str
    address: str
    state_address: str


class HAConfig(BaseModel):
    """Extracted Home Assistant configuration"""

    light: list[Light] = list()
