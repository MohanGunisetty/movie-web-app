from app.database import engine, SessionLocal
from app import models, auth, config

def init_db():
    db = SessionLocal()
    
    # Check if admin exists
    admin_email = config.settings.ADMIN_EMAIL
    admin = db.query(models.User).filter(models.User.email == admin_email).first()
    
    if not admin:
        print(f"Creating default admin user: {admin_email}")
        hashed_pw = auth.get_password_hash(config.settings.ADMIN_PASSWORD)
        admin_user = models.User(
            email=admin_email,
            username=config.settings.ADMIN_USERNAME,
            password_hash=hashed_pw,
            role=models.UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        
        # Create default categories
        categories = ["Action", "Comedy", "Drama", "Sci-Fi", "Horror", "Documentary"]
        for cat_name in categories:
            if not db.query(models.Category).filter(models.Category.name == cat_name).first():
                db.add(models.Category(name=cat_name))
        
        db.commit()
        print("Database initialized successfully.")
    else:
        print("Admin user already exists. Skipping initialization.")
    
    db.close()

if __name__ == "__main__":
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    init_db()
