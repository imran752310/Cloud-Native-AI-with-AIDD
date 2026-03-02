from sqlmodel import create_engine, Session
from app.core.config import DB_URL

engine = create_engine(DB_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session