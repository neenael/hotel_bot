from peewee import *
import os
db = SqliteDatabase(os.path.join('database', 'history.db'))


class BaseModel(Model):
    class Meta:
        database = db


class Request(BaseModel):
    class Meta:
        db_table = 'requests'
    telegram_id = IntegerField()
    request_time = CharField()
    request_date = DateField()
    checkin = DateField()
    checkout = DateField()
    mode = CharField()
    location_id = IntegerField()
    city_en = CharField()
    city_ru = CharField()
    hotels_num = IntegerField()
    photo_nes = BooleanField()
    photos_num = IntegerField(null=True)
    min_price = FloatField(null=True)
    max_price = FloatField(null=True)
    min_distance = FloatField(null=True)
    max_distance = FloatField(null=True)


db.create_tables([Request])
