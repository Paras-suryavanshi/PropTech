from app import create_app
from app.extensions import db
from app.models import User, Ticket, ActivityLog, Announcement # Importing all models ensures tables are built
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # 1. Create all tables (if they already exist, this safely does nothing)
    db.create_all()
    
    # 2. Check if the database is empty by looking for our Manager account
    if not User.query.filter_by(username='manager_demo').first():
        print("🚀 New or empty database detected! Auto-seeding demo accounts...")
        
        # Create Demo Manager
        manager = User(
            username='manager_demo', 
            full_name='Demo Manager',
            email='manager@qwego.com',
            phone_number='555-0101',
            password_hash=generate_password_hash('password123'), 
            role='manager',
            is_approved=True 
        )

        # Create Demo Tenant
        tenant = User(
            username='tenant_demo', 
            full_name='Demo Tenant',
            email='tenant@qwego.com',
            phone_number='555-0102',
            password_hash=generate_password_hash('password123'), 
            role='tenant',
            is_approved=True 
        )

        # Create Demo Technician
        tech = User(
            username='tech_demo', 
            full_name='Demo Technician',
            email='tech@qwego.com',
            phone_number='555-0103',
            password_hash=generate_password_hash('password123'), 
            role='technician',
            is_approved=True 
        )
        
        # Add them all to the database at once
        db.session.add_all([manager, tenant, tech])
        db.session.commit()
        
        print("✅ Auto-seed complete. Demo accounts are ready!")

if __name__ == '__main__':
    app.run(debug=True)