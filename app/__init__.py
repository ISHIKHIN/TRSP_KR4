from app.database import engine, Base
from app.models import Product  # noqa

def create_tables():
    Base.metadata.create_all(bind=engine)