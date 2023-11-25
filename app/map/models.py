from dataclasses import dataclass
from typing import Optional

from app.store.database.sqlalchemy_base import db

from sqlalchemy import Column, BigInteger, String


@dataclass
class MapCell:
    x: int | None
    y: int | None
    terrain_type: str | None
    resource_name: str | None


class MapCellModel(db):
    __tablename__ = "map"
    id = Column(BigInteger, primary_key = True)
    x = Column(BigInteger)
    y = Column(BigInteger)
    type = Column(String)
    resource = Column(String)
