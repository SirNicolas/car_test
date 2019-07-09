from gino import Gino
from sqlalchemy.dialects.postgresql.json import JSONB

db = Gino()


class Car(db.Model):
    __tablename__ = 'car'

    serial_number = db.Column(db.Integer(), primary_key=True)
    owner_name = db.Column(db.Unicode(), nullable=False)
    model_year = db.Column(db.Integer())
    code = db.Column(db.String())
    vehicle_code = db.Column(db.String())
    manufacturer = db.Column(db.String())
    model = db.Column(db.String())
    activation_code = db.Column(db.String())
    engine = db.Column(JSONB)
    fuel_figures = db.Column(JSONB)
    performance_figures = db.Column(JSONB)

    def to_dict(self):
        return self.__values__
