from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from .app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class MeasuringSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(32))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    samples = db.relationship('Sample', backref='measuring_set', lazy='dynamic')


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measuring_set_id = db.Column(db.Integer, db.ForeignKey('measuring_set.id'))
    create_time = db.Column(db.String(32))
    sample_name = db.Column(db.String(32))
    operator = db.Column(db.String(32))
    mass = db.Column(db.Float)
    vlazhnost = db.Column(db.Float)
    atmosphere_pressure = db.Column(db.Float)
    atmosphere_pressure_1 = db.Column(db.Float)
    graduation_name = db.Column(db.Integer)
    graduation_time = db.Column(db.String(32))
    summarnyy_raskhod = db.Column(db.Float)
    idk = db.Column(db.Float)
    idk1 = db.Column(db.Float)
    temperature = db.Column(db.Float)  # "T, K"
    density = db.Column(db.Float)
    l_to_d = db.Column(db.Float)  # "L/D"
    points = db.relationship('SamplePoint', backref='sample', lazy='dynamic')


class SamplePoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'))
    start_time = db.Column(db.String(32))
    finish_time = db.Column(db.String(32))
    p_p0 = db.Column(db.Float)
    peak_start = db.Column(db.Integer)
    peak_finish = db.Column(db.Integer)
    pick_max = db.Column(db.Integer)
    pick_amplitude = db.Column(db.Float)
    S_of_pick = db.Column(db.Float)
    grad_koeff = db.Column(db.Float)
    adsorb_or_desorb = db.Column(db.Integer)
    volume = db.Column(db.Float)
