from aiohttp.web_app import Application


def setup_routes(app: Application):
    from app.map.routes import setup_routes as map_setup_routes

    map_setup_routes(app)
