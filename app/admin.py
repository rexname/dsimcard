from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, UserDevice, Phones, db
from functools import wraps
import re

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@login_required
@admin_required
def index():
    users = User.query.all()
    phones = Phones.query.all()
    # Natural sort by ID
    def natural_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s.ID)]
    phones = sorted(phones, key=natural_key)
    return render_template('admin/index.html', users=users, phones=phones)

@admin_bp.route('/admin/user/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'error')
        return redirect(url_for('admin.index'))
    
    user = User(username=username, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    flash('User added successfully', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/admin/user/<int:user_id>/assign', methods=['POST'])
@login_required
@admin_required
def assign_devices(user_id):
    user = User.query.get_or_404(user_id)
    
    # Clear existing assignments
    UserDevice.query.filter_by(user_id=user_id).delete()
    
    # Add new assignments
    device_ids = request.form.getlist('devices')
    for device_id in device_ids:
        assignment = UserDevice(user_id=user_id, phone_id=device_id)
        db.session.add(assignment)
    
    db.session.commit()
    flash('Device assignments updated', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Don't allow deleting self
    if user.id == current_user.id:
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('admin.index'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin.index'))