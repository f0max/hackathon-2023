import typing

from app.map.views import (
    MapCellInfoView,
    DroneInfoView,
    DroneMoveView,
    DroneScanningView,
    StationInfoView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view("/map.cell_info", MapCellInfoView)
    app.router.add_view("/drone.position", DroneInfoView)
    app.router.add_view("/drone.move", DroneMoveView)
    app.router.add_view("/drone.scanning", DroneScanningView)
    app.router.add_view("/station.listen", StationInfoView)

    app.router.add_static("/images/", path='./images', name='images')
