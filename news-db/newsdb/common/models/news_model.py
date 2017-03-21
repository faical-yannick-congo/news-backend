import datetime
from ..core import db
from ..models import Radio, Coverage
import json
from bson import ObjectId

class News(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    updated_at = db.StringField(default=str(datetime.datetime.utcnow()))
    day = db.StringField()
    country = db.StringField()
    radio = db.ReferenceField(Radio, required=True)
    coverage = db.ReferenceField(Coverage, required=True)
    content = db.StringField()
    possible_status = ["pushed", "pushing", "pulled"]
    status = db.StringField(default="pulled", choices=possible_status)
    received = db.IntField(default=0)
    possible_schedule_hour = ["24:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    schedule = db.StringField(default="6:00", choices=possible_schedule_hour)
    importance = db.IntField(default=0)

    def save(self, *args, **kwargs):
        self.updated_at = str(datetime.datetime.utcnow())
        return super(News, self).save(*args, **kwargs)

    def info(self):
        data = {'updated-at':self.updated_at, 'id':str(self.id),
        'content':self.content, 'status':self.status, 'day':self.day, 'coverage':str(self.coverage.id),
        'radio':self.radio.info(), 'received':self.received, 'country':self.country, 'schedule':self.schedule,
        'importance':self.importance}
        return data

    def to_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
