from app import create_app, db
from app.models.user import UserModel

app = create_app()
with app.app_context():
    # Créer l'utilisateur admin
    admin = UserModel(
        first_name='Admin',
        last_name='HBnB',
        email='admin@hbnb.io',
        is_admin=True
    )
    admin.hash_password('admin123')  # Hash le mot de passe
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Admin créé avec succès! ID: {admin.id}")
