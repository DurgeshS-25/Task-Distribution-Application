from pydantic import BaseModel, EmailStr, constr,field_validator
from typing import Annotated

# Password constraints (bcrypt limit = 72 chars)
# - At least 1 uppercase
# - At least 1 lowercase
# - At least 1 digit
# - At least 1 special character


PasswordStr = constr(min_length=8, max_length=72)


#--------- Invite ----------
class InviteRequest(BaseModel):
    email: EmailStr


# ---------- Signup ----------  
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: PasswordStr
    token: str

    @field_validator("password")
    def validate_password(cls, value):
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "@$!%*?&" for c in value):
            raise ValueError("Password must contain at least one special character (@$!%*?&)")
        return value
# ---------- User Schemas ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: PasswordStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True


# ---------- Auth Token ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
