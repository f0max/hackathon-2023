from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class PositionRequestSchema(Schema):
    x = fields.Int(required=True)
    y = fields.Int(required=True)


class MapCellSchema(Schema):
    x = fields.Int(required=True)
    y = fields.Int(required=True)
    terrain_type = fields.Str(required=True)
    resource_name = fields.Str(required=True)

class MapCellResponseSchema(OkResponseSchema):
    data = fields.Nested(MapCellSchema)

class MapCellListSchema(OkResponseSchema):
    data = fields.Nested(MapCellSchema, many=True)

class DronePositionResponseSchema(OkResponseSchema):
    data = fields.Nested(PositionRequestSchema)

class DroneMoveResponseSchema(OkResponseSchema):
    data = fields.Str()

class DroneScanningResponseSchema(OkResponseSchema):
    data = fields.Nested(MapCellSchema)
