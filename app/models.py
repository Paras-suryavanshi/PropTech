from .extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    # Role can be: 'tenant', 'manager', 'technician'
    role = db.Column(db.String(20), nullable=False)
    # Approval Status. Defaults to False when someone registers!
    is_approved = db.Column(db.Boolean, default=False)
    # setup backrefs for easier querying later
    tickets_created = db.relationship('Ticket', foreign_keys='Ticket.tenant_id', backref='tenant', lazy=True)
    tickets_assigned = db.relationship('Ticket', foreign_keys='Ticket.technician_id', backref='technician', lazy=True)
    announcements = db.relationship('Announcement', backref='author', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    # Status flow: Open -> Assigned -> In Progress -> Done
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign keys link this ticket to specific users
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # Relationship to the activity log
    logs = db.relationship('ActivityLog', backref='ticket', lazy=True)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False) # e.g., "Ticket Created" or "Status changed to Done"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    target_role = db.Column(db.String(20), nullable=False) # Will be 'tenant', 'technician', or 'all'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

from .extensions import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))