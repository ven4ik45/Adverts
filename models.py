from datetime import datetime
from decouple import config

from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from atexit import register

POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
POSTGRES_DB = config("POSTGRES_DB")
POSTGRES_HOST = config("POSTGRES_HOST")
POSTGRES_PORT = config("POSTGRES_PORT")

PG_DSN = f"postgresql://" \
         f"{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
         f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Adverts(Base):
    __tablename__ = "app_adverts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(128), nullable=True)
    owner: Mapped[str] = mapped_column(String(24), nullable=False)
    data_create: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner": self.owner,
            "data_create": self.data_create.isoformat(),
        }


Base.metadata.create_all(bind=engine)

register(engine.dispose)