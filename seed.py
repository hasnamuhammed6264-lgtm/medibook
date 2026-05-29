from app import create_app, db, bcrypt
from app.models import User, Doctor

app = create_app()

with app.app_context():
    # Create doctor users
    doctors_data = [
        {
            "full_name": "Dr. Arjun Sharma",
            "email": "arjun@medibook.com",
            "specialty": "Cardiologist",
            "bio": "15 years experience in heart diseases and cardiac surgery.",
            "experience": 15,
            "fee": 800
        },
        {
            "full_name": "Dr. Priya Nair",
            "email": "priya@medibook.com",
            "specialty": "Dermatologist",
            "bio": "Expert in skin conditions, cosmetic and medical dermatology.",
            "experience": 10,
            "fee": 600
        },
        {
            "full_name": "Dr. Rahul Menon",
            "email": "rahul@medibook.com",
            "specialty": "Orthopedist",
            "bio": "Specialist in bone, joint and muscle treatments.",
            "experience": 12,
            "fee": 700
        },
        {
            "full_name": "Dr. Sneha Pillai",
            "email": "sneha@medibook.com",
            "specialty": "Pediatrician",
            "bio": "Dedicated to child health from newborns to teenagers.",
            "experience": 8,
            "fee": 500
        },
        {
            "full_name": "Dr. Vikram Das",
            "email": "vikram@medibook.com",
            "specialty": "Neurologist",
            "bio": "Expert in brain, spine and nervous system disorders.",
            "experience": 18,
            "fee": 1000
        },
    ]

    for d in doctors_data:
        # Check if user already exists
        existing = User.query.filter_by(email=d['email']).first()
        if not existing:
            pw = bcrypt.generate_password_hash('doctor123').decode('utf-8')
            user = User(
                full_name=d['full_name'],
                email=d['email'],
                password=pw,
                role='doctor'
            )
            db.session.add(user)
            db.session.flush()

            doctor = Doctor(
                user_id=user.id,
                specialty=d['specialty'],
                bio=d['bio'],
                experience=d['experience'],
                fee=d['fee'],
                available=True
            )
            db.session.add(doctor)

    # Create admin user
    admin_exists = User.query.filter_by(email='admin@medibook.com').first()
    if not admin_exists:
        pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            full_name='Admin',
            email='admin@medibook.com',
            password=pw,
            role='admin'
        )
        db.session.add(admin)

    db.session.commit()
    print("✅ 5 doctors added!")
    print("✅ Admin created! Email: admin@medibook.com | Password: admin123")
    print("✅ Doctor password: doctor123")
