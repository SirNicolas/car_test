from aiohttp import web
from aiohttp_validate import validate

from car_info.schema import CAR_POST_SCHEMA, CAR_PATCH_SCHEMA
from car_info.logic import (
    create_car, get_all_cars, get_car, patch_car, delete_car,
)

routes = web.RouteTableDef()


@routes.get('/car')
async def get_all(request):
    cars = await get_all_cars()
    return web.json_response({'elements': [car.to_dict() for car in cars]})


@routes.post('/car')
@validate(request_schema=CAR_POST_SCHEMA)
async def create(data, request):
    car = await create_car(data)
    return web.json_response(car.to_dict())


@routes.get(r'/car/{serial_number:\d+}')
async def get(request):
    car = await get_car(int(request.match_info['serial_number']))
    return web.json_response(car.to_dict())


@routes.patch(r'/car/{serial_number:\d+}')
@validate(request_schema=CAR_PATCH_SCHEMA)
async def patch(data, request):
    car = await patch_car(int(request.match_info['serial_number']), data)
    return web.json_response(car.to_dict())


@routes.delete(r'/car/{serial_number:\d+}')
async def delete(request):
    await delete_car(int(request.match_info['serial_number']))
    return web.HTTPNoContent()
