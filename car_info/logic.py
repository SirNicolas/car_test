from typing import List
from aiohttp import web
from asyncpg.exceptions import UniqueViolationError

from car_info.model import Car


async def create_car(data: dict) -> Car:
    try:
        car = await Car.create(**data)
    except UniqueViolationError:
        raise web.HTTPBadRequest(
            reason=f'Car with {data["serial_number"]} already exists'
        )
    return car


async def get_all_cars() -> List[Car]:
    return await Car.query.gino.all()


async def get_car(serial_number: int) -> Car:
    car = await Car.query.where(
            Car.serial_number == serial_number
        ).gino.first()
    if not car:
        raise web.HTTPNotFound
    return car


async def patch_car(serial_number: int, data: dict) -> Car:
    car = await get_car(serial_number)
    await car.update(**data).apply()
    return car


async def delete_car(serial_number: int):
    car = await get_car(serial_number)
    await car.delete()
