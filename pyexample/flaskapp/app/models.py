from .extensions import db
from datetime import datetime

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String(11), unique=True, index=True)
    phone_code = db.Column(db.String(4))
    session_id = db.Column(db.String(256))
    create_at = db.Column(db.DateTime, default=datetime.now)
    modify_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    uuid = db.Column(db.String(36))
    userid_type = db.Column(db.Integer)


    def set_session_id(self):
        raise NotImplementedError

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_sec_uuid(self):
        raise NotImplementedError
    

    @property
    def apiclient(self):
        raise NotImplementedError