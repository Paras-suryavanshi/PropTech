# 🏢 PropTech: Smart Property Maintenance 

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Mobile First](https://img.shields.io/badge/Design-Mobile%20First-success?style=for-the-badge)

A full-stack, B2B SaaS platform designed to eliminate the chaos of property maintenance.PropTech connects Property Managers, Tenants, and Technicians through a secure, role-based, and strictly enforced workflow ecosystem.

---

## 🎯 The Problem
Property maintenance today is broken. Tenants send vague text messages ("the sink is leaking"), managers lose track of who was assigned to what, and technicians show up without knowing the full history of the issue. The result is delayed repairs, frustrated renters, and inefficient use of capital.

## 🧠 Our Approach & Methodology
I approached this problem by focusing on **Data Strictness** and **Frictionless UX**. 

1. **Zero-Ambiguity Data:** Tenants *cannot* submit a ticket without photographic evidence. Technicians *cannot* mark a job as "Done" without first officially marking it "In Progress." We let the software enforce the rules so managers don't have to.
2. **Tripartite Architecture:** We built three distinct dashboards tailored to the exact psychological needs of each user role. 
3. **Secure Gatekeeping:** To protect tenant privacy and ensure quality control, technician accounts are completely sandboxed upon creation. A technician cannot view tickets or access their dashboard until a Manager explicitly verifies and approves their profile.
4. **Mobile-First Reality:** Maintenance doesn't happen at a desk. We engineered a 100% responsive UI ensuring tenants can upload photos from their phones and technicians can update statuses from the field.

---

## 🔄 The Core Workflow Explained
Our system operates on a seamless, traceable lifecycle:

* **Phase 1: Reporting (The Tenant)**
  Tenants log in, write a description, and are forced to upload a mandatory image. The system auto-generates a ticket with an "Open" status.
* **Phase 2: Triage & Assignment (The Manager)**
  The Manager dashboard aggregates all open tickets. The manager selects an available, verified technician from the directory and assigns the job.
* **Phase 3: Execution (The Technician)**
  The Technician sees the job in their queue. To ensure accurate time-tracking, the UI strictly requires them to click **"In Progress"** before the **"Mark as Done"** button is unlocked.
* **Phase 4: The Audit Trail (System Automated)**
  Behind the scenes, the `ActivityLog` engine silently records every state change, timestamp, and actor, rendering a visual timeline on the ticket for complete transparency.

---

## ✨ Key Features

* **Role-Based Access Control (RBAC):** Securely isolated environments for Managers, Tenants, and Techs.
* **Admin Gatekeeping:** New technician accounts are quarantined in a "Pending" state until manually verified by a Manager. (Tenants are auto-approved to reduce onboarding friction).
* **Targeted Broadcast System:** A centralized communication hub allowing managers to blast priority announcements to all users, or filter by specific roles (e.g., "Technicians Only").
* **Smart Auto-Seeding:** The application detects empty database states and autonomously injects demo accounts for instant evaluation.
* **Strict Validation:** Dual-layer (Frontend HTML5 + Backend Python) validation preventing incomplete data entries.

---

## 🚀 Live Demo For Evaluators
I value your time. You can completely bypass the registration and approval process by using my pre-configured demo accounts to test the application instantly:

| Role | Username | Password | Key Actions to Test |
| :--- | :--- | :--- | :--- |
| **Manager** | `manager_demo` | `password123` | Assign jobs, broadcast announcements, view directory. |
| **Tenant** | `tenant_demo` | `password123` | Report an issue, upload a photo, view activity timeline. |
| **Technician**| `tech_demo` | `password123` | View assigned jobs, unlock the 'Done' button. |

---

## 🛠️ Technical Stack
* **Backend:** Python 3, Flask
* **Database:** PostgreSQL (Production) / SQLite (Local Dev), SQLAlchemy ORM
* **Authentication:** Flask-Login, Werkzeug Security (Password Hashing)
* **Frontend:** HTML5, CSS3, Jinja2 Templating, Custom CSS Media Queries

---

## 🔮 Future Scope
While the current MVP solves the core operational bottleneck, our roadmap includes:
1. **AI Triage & Routing:** Implementing machine learning to analyze the tenant's issue title, description and uploaded photo and automatically suggest the correct technician type (Plumber, Electrician, etc.).
2. **In-App Messaging:** Real-time, socket-based chat between the assigned technician and the tenant for gate codes or ETA updates.
3. **Invoicing Integration:** Automated generation of PDF invoices sent to the manager the moment a technician marks a job as "Done."
4. **IoT Integration:** Allowing smart building sensors (e.g., water leak detectors) to automatically generate high-priority API tickets without human intervention.

---

# Local Setup Instructions

1. Clone the repository: Open your terminal and type git clone <your-repo-link>, then navigate into the folder by typing cd <your-repo-folder>.

2. Set up a virtual environment: Type python -m venv venv to create the isolated environment. To activate it, type source venv/bin/activate (or use venv\Scripts\activate if you are on Windows).

3. Install dependencies: Type pip install -r requirements.txt to install all required packages.

4. Configure Environment: Create a file named .env in the root directory. Inside that file, add your database URI and secret key on separate lines, exactly like this:
DATABASE_URL=postgresql://user:password@localhost:5432/proptech
SECRET_KEY=your_secret_key

5. Run the Application: Type python run.py to start the server.
(Note: The system will automatically detect an empty database and seed the demo accounts upon the first run).