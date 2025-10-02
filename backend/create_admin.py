import sys
from getpass import getpass
from sqlalchemy.orm import Session
from app import models, utils, database   # ✅ this now works since we're in backend/

def create_admin():
    db: Session = database.SessionLocal()

    email = input("Enter admin email: ").strip()
    name = input("Enter admin name: ").strip()
    password = getpass("Enter admin password: ")

    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        print("❌ Admin with this email already exists!")
        sys.exit(1)

    admin = models.User(
        name=name,
        email=email,
        password_hash=utils.hash_password(password),
        role="admin",
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    print(f"✅ Admin created successfully: {admin.email} (id={admin.id})")
    db.close()

if __name__ == "__main__":
    create_admin()
