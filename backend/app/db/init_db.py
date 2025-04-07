from sqlalchemy import create_engine
from ..models.base import Base
from ..core.config import settings

def init_db():
    engine = create_engine(settings.SQLITE_DATABASE_URL)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db() 