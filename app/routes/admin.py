from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Doctor, Appointment

admin = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access only!', 'danger')
            return redirect(url_for('auth.home'))
        return f(*args, **kwargs)
    return decorated

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    total_patients      = User.query.filter_by(role='patient').count()
    total_doctors       = Doctor.query.count()
    total_appointments  = Appointment.query.count()
    pending_appointments= Appointment.query.filter_by(status='pending').count()
    appointments        = Appointment.query.order_by(Appointment.date.desc()).all()
    users               = User.query.order_by(User.created_at.desc()).all()

    return render_template('admin_dashboard.html',
        title='Admin Dashboard',
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        pending_appointments=pending_appointments,
        appointments=appointments,
        users=users
    )

@admin.route('/admin/confirm/<int:apt_id>')
@login_required
@admin_required
def confirm_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    apt.status = 'confirmed'
    db.session.commit()
    flash('Appointment confirmed!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/cancel/<int:apt_id>')
@login_required
@admin_required
def cancel_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    apt.status = 'cancelled'
    db.session.commit()
    flash('Appointment cancelled.', 'info')
    return redirect(url_for('admin.dashboard'))
