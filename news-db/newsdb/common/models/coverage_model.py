import datetime
from ..core import db
from ..models import Radio
import json
from bson import ObjectId

class Coverage(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    updated_at = db.StringField(default=str(datetime.datetime.utcnow()))
    name = db.StringField()
    radios = db.ListField(db.ReferenceField(Radio))
    zone = db.StringField() # Based on GMT
    country = db.StringField()
    possible_schedule_hour = ["24:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    schedule = db.ListField(db.StringField(default="6:00", choices=possible_schedule_hour)) # List of hours in the day for the news
    synchronization = db.ListField(db.StringField())
    delivery = db.ListField(db.StringField())

    def save(self, *args, **kwargs):
        self.updated_at = str(datetime.datetime.utcnow())
        return super(Coverage, self).save(*args, **kwargs)

    def info(self):
        data = {'updated-at':self.updated_at, 'id':str(self.id),
        'created_at':self.created_at, 'radios':[radio.info() for radio in self.radios], 'name':self.name,
        'zone':self.zone, 'country':self.country, 'schedule':self.schedule, 'delivery':self.delivery,
        'sync':self.synchronization}
        return data

    def to_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
