import pytest
from copy import deepcopy
from car_info.config import config
from car_info.model import db, Car
from car_info.app import make_app

first_car = {'serial_number': 123, "owner_name": "Vasya"}
second_car = {'serial_number': 124, "owner_name": "Petya"}


@pytest.fixture(scope='function')
async def setup_db():
    await db.set_bind(
        f'postgresql://{config["dbconfig"]["host"]}/'
        f'{config["dbconfig"]["testdb"]}'
    )
    await db.gino.drop_all()
    await db.gino.create_all()
    await Car.create(**first_car)
    await Car.create(**second_car)


@pytest.fixture(scope='function')
async def fx_client(aiohttp_client, setup_db):
    app = make_app()
    client = await aiohttp_client(app)

    return client


async def test_get_all_cars(fx_client):
    resp = await fx_client.get('/car')
    assert resp.status == 200
    text = await resp.json()
    assert 'elements' in text
    assert text == {
        "elements": [{
            "serial_number": 123, "owner_name": "Vasya",
            "model_year": None, "code": None, "vehicle_code": None,
            "manufacturer": None, "model": None,
            "activation_code": None, "engine": None,
            "fuel_figures": None, "performance_figures": None
        }, {
            "serial_number": 124, "owner_name": "Petya",
            "model_year": None, "code": None, "vehicle_code": None,
            "manufacturer": None, "model": None,
            "activation_code": None, "engine": None,
            "fuel_figures": None, "performance_figures": None
        }]
    }


async def test_success_post_car(fx_client):
    car = {
        "owner_name": "Grigoriy", "serial_number": 534,
        "engine": {"capacity": 1, "num_cylinders": 2}
    }
    resp = await fx_client.post('/car', json=car)
    assert resp.status == 200
    text = await resp.json()
    assert text == {
        'activation_code': None,
        'code': None,
        'engine': {'capacity': 1, 'num_cylinders': 2},
        'fuel_figures': None,
        'manufacturer': None,
        'model': None,
        'model_year': None,
        'owner_name': 'Grigoriy',
        'performance_figures': None,
        'serial_number': 534,
        'vehicle_code': None
    }


async def test_invalid_post_car(fx_client):
    missed_owner_name = {
        "serial_number": 123,
        "engine": {"capacity": 1, "num_cylinders": 2}
    }
    resp = await fx_client.post('/car', json=missed_owner_name)
    assert resp.status == 400

    serial_number_already_exists = {
        "owner_name": "Grigoriy", "serial_number": 123,
        "engine": {"capacity": 1, "num_cylinders": 2}
    }
    resp = await fx_client.post('/car', json=serial_number_already_exists)
    assert resp.status == 400


async def test_get_car(fx_client):
    resp = await fx_client.get(f'/car/{first_car["serial_number"]}')
    assert resp.status == 200
    text = await resp.json()
    assert text == {
        "serial_number": 123, "owner_name": "Vasya",
        "model_year": None, "code": None, "vehicle_code": None,
        "manufacturer": None, "model": None,
        "activation_code": None, "engine": None,
        "fuel_figures": None, "performance_figures": None
    }


async def test_success_patch_car(fx_client):
    car = {
        "model_year": 2019, "code": '453'
    }
    resp = await fx_client.patch(f'/car/{first_car["serial_number"]}', json=car)
    assert resp.status == 200
    text = await resp.json()
    assert text == {
        "serial_number": 123, "owner_name": "Vasya",
        "model_year": 2019, "code": "453", "vehicle_code": None,
        "manufacturer": None, "model": None,
        "activation_code": None, "engine": None,
        "fuel_figures": None, "performance_figures": None
    }


async def test_invalid_patch_car(fx_client):
    invalid_type = {
        "model_year": '2019'
    }
    resp = await fx_client.patch(
        f'/car/{first_car["serial_number"]}',
        json=invalid_type
    )
    assert resp.status == 400

    extra_param = {
        "popularity": 'max'
    }
    resp = await fx_client.patch(
        f'/car/{first_car["serial_number"]}',
        json=extra_param
    )
    assert resp.status == 400


async def test_success_delete(fx_client):
    resp = await fx_client.delete(f'/car/{first_car["serial_number"]}')
    assert resp.status == 204


async def test_not_found_car(fx_client):
    resp = await fx_client.get('/car/100500')
    assert resp.status == 404
