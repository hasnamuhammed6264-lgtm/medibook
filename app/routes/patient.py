from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Doctor, Appointment
from datetime import date, datetime

patient = Blueprint('patient', __name__)

@patient.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@patient.route('/doctors')
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', title='Doctors', doctors=all_doctors)

@patient.route('/book/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        apt_date_str = request.form.get('date')
        time_slot    = request.form.get('time_slot')
        reason       = request.form.get('reason')

        # ✅ Fix: convert string to Python date object
        apt_date = datetime.strptime(apt_date_str, '%Y-%m-%d').date()

        # Check for duplicate booking
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=apt_date,
            time_slot=time_slot
        ).first()
        if existing:
            flash('That time slot is already booked. Please choose another.', 'warning')
            return redirect(url_for('patient.book', doctor_id=doctor_id))

        apt = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor_id,
            date=apt_date,
            time_slot=time_slot,
            reason=reason,
            status='pending'
        )
        db.session.add(apt)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient.my_appointments'))

    return render_template('book_appointment.html',
                           title='Book Appointment',
                           doctor=doctor,
                           today=date.today())

@patient.route('/my-appointments')
@login_required
def my_appointments():
    appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).order_by(Appointment.date.desc()).all()
    return render_template('my_appointments.html',
                           title='My Appointments',
                           appointments=appointments)

@patient.route('/cancel/<int:apt_id>')
@login_required
def cancel(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    if apt.patient_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('patient.my_appointments'))
    apt.status = 'cancelled'
    db.session.commit()
    flash('Appointment cancelled.', 'info')
    return redirect(url_for('patient.my_appointments'))
