import os
from werkzeug.utils import secure_filename
from flask import current_app, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import main_bp
from ..extensions import db
from ..models import User, Ticket, ActivityLog, Announcement

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # 1. Gatekeeper Check
    if not current_user.is_approved:
        return render_template('main/pending.html') # We will make this simple HTML later

    # 2. Manager Dashboard Logic
    if current_user.role == 'manager':
        # Get all users who need approval
        pending_users = User.query.filter_by(is_approved=False).all()
        # fetch all tickets - optimize this query later
        all_tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
        # get verified techs for the assignment dropdown
        technicians = User.query.filter_by(role='technician', is_approved=True).all()
        
        return render_template('main/manager_dashboard.html', 
                               pending_users=pending_users, 
                               tickets=all_tickets,
                               technicians=technicians)

    # handle tenant flow
    elif current_user.role == 'tenant':
        # get their specific tickets only
        my_tickets = Ticket.query.filter_by(tenant_id=current_user.id).order_by(Ticket.created_at.desc()).all()
        # Fetch announcements for 'tenant' or 'all'
        announcements = Announcement.query.filter(Announcement.target_role.in_(['tenant', 'all'])).order_by(Announcement.created_at.desc()).all()
        return render_template('main/tenant_dashboard.html', tickets=my_tickets, announcements=announcements)

    # tech dashboard stuff
    elif current_user.role == 'technician':
        # Fetch ONLY the tickets assigned to this specific technician
        my_jobs = Ticket.query.filter_by(technician_id=current_user.id).order_by(Ticket.created_at.desc()).all()
        # Fetch announcements for 'technician' or 'all'
        announcements = Announcement.query.filter(Announcement.target_role.in_(['technician', 'all'])).order_by(Announcement.created_at.desc()).all()
        return render_template('main/technician_dashboard.html', tickets=my_jobs, announcements=announcements)

# common profile page
@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')

# --- The Approval Action ---
@main_bp.route('/approve_user/<int:user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    # Security check: ONLY managers can trigger this route!
    if current_user.role != 'manager':
        flash("Unauthorized action.")
        return redirect(url_for('main.dashboard'))

    user_to_approve = User.query.get_or_404(user_id)
    user_to_approve.is_approved = True
    db.session.commit()
    
    flash(f"User {user_to_approve.username} has been approved!")
    return redirect(url_for('main.dashboard'))

# --- Create Ticket ---
@main_bp.route('/create-ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if current_user.role != 'tenant' or not current_user.is_approved:
        flash("Unauthorized access.")
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        # --- NEW STRICT IMAGE VALIDATION ---
        # 1. Check if the file part is even in the request
        if 'image' not in request.files:
            flash('An image upload is mandatory to report an issue.')
            return redirect(request.url)
            
        file = request.files.get('image')
        
        # 2. Check if they submitted an empty form without selecting a file
        if file.filename == '':
            flash('No selected image file. Please choose a photo.')
            return redirect(request.url)

        # 3. If it passes both checks, save it securely!
        filename = secure_filename(file.filename)
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        # -----------------------------------

        # Save to Database
        new_ticket = Ticket(
            title=title,
            description=description,
            image_filename=filename,
            tenant_id=current_user.id
        )
        db.session.add(new_ticket)
        db.session.commit()

        # Save to Activity Log
        log = ActivityLog(
            ticket_id=new_ticket.id, 
            actor_id=current_user.id, 
            action="Ticket Submitted by Tenant"
        )
        db.session.add(log)
        db.session.commit()

        flash('Maintenance ticket submitted successfully!')
        return redirect(url_for('main.dashboard'))

    return render_template('main/create_ticket.html')

# --- Assign Ticket to Technician ---
@main_bp.route('/assign_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def assign_ticket(ticket_id):
    # Security: Only managers can assign tickets
    if current_user.role != 'manager':
        flash("Unauthorized action.")
        return redirect(url_for('main.dashboard'))

    ticket = Ticket.query.get_or_404(ticket_id)
    tech_id = request.form.get('technician_id')

    if tech_id:
        # Update the ticket
        ticket.technician_id = tech_id
        ticket.status = 'assigned'

        # Log the activity
        tech_user = User.query.get(tech_id)
        log = ActivityLog(
            ticket_id=ticket.id,
            actor_id=current_user.id,
            action=f"Assigned to Technician {tech_user.full_name}."
        )      
        db.session.add(log)
        db.session.commit()

        flash(f"Ticket '{ticket.title}' assigned to {tech_user.full_name}.")       
    return redirect(url_for('main.dashboard'))

# --- Update Ticket Status (Technician Only) ---
@main_bp.route('/update_status/<int:ticket_id>', methods=['POST'])
@login_required
def update_status(ticket_id):
    # Security check: Only technicians can trigger this
    if current_user.role != 'technician':
        flash("Unauthorized action.")
        return redirect(url_for('main.dashboard'))

    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form.get('status')

    # Security check: Make sure they aren't updating someone else's ticket!
    if ticket.technician_id != current_user.id:
        flash("You can only update tickets assigned to you.")
        return redirect(url_for('main.dashboard'))

    # Update the status if it's a valid progression
    if new_status in ['In Progress', 'Done']:
        ticket.status = new_status
        
        # Log the activity
        log = ActivityLog(
            ticket_id=ticket.id, 
            actor_id=current_user.id, 
            action=f"Status updated to: {new_status}"
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f"Job '{ticket.title}' is now {new_status}!")
    
    return redirect(url_for('main.dashboard'))

# --- Post Announcement (Manager Only) ---
@main_bp.route('/post_announcement', methods=['POST'])
@login_required
def post_announcement():
    if current_user.role != 'manager':
        flash("Unauthorized action.")
        return redirect(url_for('main.dashboard'))

    title = request.form.get('title')
    message = request.form.get('message')
    target_role = request.form.get('target_role')

    new_announcement = Announcement(
        title=title,
        message=message,
        target_role=target_role,
        manager_id=current_user.id
    )
    db.session.add(new_announcement)
    db.session.commit()
    
    flash('Announcement broadcasted successfully!')
    return redirect(url_for('main.dashboard'))