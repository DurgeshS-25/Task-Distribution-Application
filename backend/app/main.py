from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uuid
from app.auth import admin_required
from app import models, schemas, utils, database
from app.schemas import InviteRequest, SignupRequest

from jose import JWTError, jwt

app = FastAPI()

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

# ---------- DB Dependency ----------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Root ----------
@app.get("/")
def root():
    return {"message": "Task Assign API is running 🚀"}

# ---------- Admin Invite ----------
@app.post("/admin/invite")
def create_invite(
    request: InviteRequest, 
    db: Session = Depends(get_db), 
    _: models.User = Depends(admin_required)  # 👈 only admin can invite
):
    existing = db.query(models.Invite).filter(models.Invite.email == request.email).first()
    token = str(uuid.uuid4())

    if existing:
        existing.token = token
        existing.is_used = False
        db.commit()
        db.refresh(existing)
        return {"invite_link": f"http://127.0.0.1:8000/signup?token={token}"}

    invite = models.Invite(email=request.email, token=token, is_used=False)
    db.add(invite)
    db.commit()
    db.refresh(invite)

    return {"invite_link": f"http://127.0.0.1:8000/signup?token={token}"}

# ---------- Signup ----------
@app.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    invite = db.query(models.Invite).filter_by(token=request.token, is_used=False).first()
    if not invite or invite.email != request.email:
        raise HTTPException(status_code=400, detail="Invalid or expired invite")

    # Check if email already exists
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = models.User(
        name=request.name,
        email=request.email,
        password_hash=utils.hash_password(request.password),
        role="user",
        is_active=True
    )

    invite.is_used = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "Account created successfully 🎉"}

# ---------- Auth ----------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login", response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not utils.verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = utils.create_access_token(
    data={"sub": user.email, "id": user.id, "role": user.role})  # 👈 include role
    return {"access_token": access_token, "token_type": "bearer"}

# ---------- Protected Route ----------
@app.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
