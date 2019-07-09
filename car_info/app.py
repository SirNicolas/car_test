from aiohttp import web
from car_info.handlers import routes


def make_app():
    app = web.Application()
    app.add_routes(routes)
    return app
