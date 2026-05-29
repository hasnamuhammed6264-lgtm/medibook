from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password      = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20), default='patient')  # patient / doctor / admin
    phone         = db.Column(db.String(20))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    appointments  = db.relationship('Appointment', foreign_keys='Appointment.patient_id', backref='patient', lazy=True)

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialty     = db.Column(db.String(100), nullable=False)
    bio           = db.Column(db.Text)
    experience    = db.Column(db.Integer)           # years
    fee           = db.Column(db.Float, default=0)
    available     = db.Column(db.Boolean, default=True)
    photo         = db.Column(db.String(200))

    user          = db.relationship('User', backref='doctor_profile')
    appointments  = db.relationship('Appointment', foreign_keys='Appointment.doctor_id', backref='doctor', lazy=True)

    def __repr__(self):
        return f'<Doctor {self.specialty}>'


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id            = db.Column(db.Integer, primary_key=True)
    patient_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id     = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date          = db.Column(db.Date, nullable=False)
    time_slot     = db.Column(db.String(20), nullable=False)   # e.g. "10:00 AM"
    reason        = db.Column(db.Text)
    status        = db.Column(db.String(20), default='pending') # pending/confirmed/cancelled/completed
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    notes         = db.Column(db.Text)                          # doctor's notes after visit

    def __repr__(self):
        return f'<Appointment {self.date} {self.time_slot} - {self.status}>'
