import asyncio
from aiohttp import web
from car_info.app import make_app
from car_info.config import config
from car_info.model import db


async def main():
    # connect to database
    await db.set_bind(
        f'postgresql://{config["dbconfig"]["host"]}/{config["dbconfig"]["db"]}'
    )
    # create tables if they don't exist
    await db.gino.create_all()

asyncio.get_event_loop().run_until_complete(main())

if __name__ == '__main__':
    web.run_app(make_app())
