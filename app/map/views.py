import datetime as dt

from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import querystring_schema, request_schema, response_schema
from app.map.schemes import (
    PositionRequestSchema,
    MapCellSchema,
    MapCellResponseSchema,
    MapCellListSchema,
    DronePositionResponseSchema,
    DroneMoveResponseSchema,
    DroneScanningResponseSchema
)
from app.web.app import View
from app.web.utils import json_response
    

class MapCellInfoView(View):
    @response_schema(MapCellListSchema)
    async def get(self):
        maps = await self.store.maps.get_all_cells()
        return json_response(data=maps)

    @request_schema(PositionRequestSchema)
    @response_schema(MapCellResponseSchema)
    async def post(self):
        req_data = await self.request.json()
        x, y = req_data['x'], req_data['y']
        map_cell = await self.store.maps.get_cell_by_coords(x, y)
        if map_cell:
            return json_response(data=MapCellSchema().dump(map_cell))
        else:
            data = {'message': 'No info about this cell'}
            return json_response(data=data)


class DroneInfoView(View):
    @response_schema(DronePositionResponseSchema)
    async def get(self):
        coords = await self.store.maps.get_drone_position()
        return json_response(data=coords)
    
class DroneMoveView(View):
    @response_schema(DroneMoveResponseSchema)
    @request_schema(PositionRequestSchema)
    async def post(self):
        req_data = await self.request.json()
        x, y = req_data['x'], req_data['y']
        data = await self.store.maps.drone_move(x, y)
        return json_response(data=data)
    
class DroneScanningView(View):
    @response_schema(DroneScanningResponseSchema)
    async def get(self):
        data = await self.store.maps.drone_scnanning()
        return json_response(data=data)
    
class StationInfoView(View):
    async def post(self):
        req_data = await self.request.json()
        x, y = req_data['x'], req_data['y']
        #  send to front
        print('#######################')
        print(f'Station Position on {dt.datetime.now()}: {x}, {y}')
        print('#######################')
        return json_response(data=[x, y])
    