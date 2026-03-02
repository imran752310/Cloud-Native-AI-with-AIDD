from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.core.security import hash_password, verify_password
from app.api.deps import db_session

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(db_session)):
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    print(db_user)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserRead])
def get_users(session: Session = Depends(db_session)):
    return session.exec(select(User)).all()

@router.post("/login", response_model=dict)
def login_user(user: UserLogin, session: Session = Depends(db_session)):
    exsiting_user = session.exec(select(User).where(User.email == user.email)).first()
    if not exsiting_user:
        raise HTTPException(status_code=404, detail= "User Not Found")
    
   
    CheckPassword = verify_password(user.password, exsiting_user.password)
    if not CheckPassword:
        raise HTTPException(status_code=409, detail="Passwod not Valid")
    return {"Message": "Your Are Login"}