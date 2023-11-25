import aiohttp
import json
from typing import Optional
from sqlalchemy import select, update

from app.base.base_accessor import BaseAccessor
from app.map.models import (
    MapCell,
    MapCellModel
)

from app.map.schemes import MapCellSchema


API_URL = 'http://192.168.68.238:8080'

class MapAccessor(BaseAccessor):
    async def get_all_cells(self) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}/map.get_all') as resp:
                response = await resp.text()
                data = json.loads(response)['data']['maps']
            
        async with self.app.database.session() as session:
            res = await session.execute(select(MapCellModel))
            if res.scalars().all() == []:
                for cell in data:
                    new_cell = MapCellModel(x=cell['x'], y=cell['y'],
                                            type=cell['type'], resource=None)
                    session.add(new_cell)
                await session.commit()

        return data

    async def get_cell_by_coords(self, x: int, y: int) -> MapCell | None:
        async with self.app.database.session() as session:
            res = await session.execute(select(MapCellModel)
                                        .where(MapCellModel.x == x,
                                               MapCellModel.y == y))
            cell = res.scalars().first()

            if cell:
                return MapCell(x=cell.x, y=cell.y,
                                terrain_type=cell.type,
                                resource_name=cell.resource)
        return None
    
    async def get_drone_position(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}/drone.get_position') as resp:
                response = await resp.text()
                data = json.loads(response)['data']
                return {
                    "x": data[0],
                    "y": data[1]
                }
            
    async def drone_move(self, x: int, y: int):
        url = f'{API_URL}/drone.move'
        json_ = {
            "x": x,
            "y": y
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url,
                                    json=json_) as resp:
                response = await resp.text()
                data = json.loads(response)['data']
                return data

    async def drone_scnanning(self):
        coords = await self.get_drone_position()
        url = f'{API_URL}/map.get_cell'

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as resp:
                response = await resp.text()
                data = json.loads(response)['data']
        if data != 'Дрон в полёте!!!':
            async with self.app.database.session() as session:
                await session.execute(update(MapCellModel)
                                    .where(MapCellModel.x == coords['x'],
                                            MapCellModel.y == coords['y'])
                                    .values(resource = data['resource']))
                await session.commit()

        return data

    