from waitress import serve
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

print("🚀 MediBook running on http://0.0.0.0:5000")
serve(app, host='0.0.0.0', port=5000)
