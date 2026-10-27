import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def _resolver_sqlite_url(database_url: str) -> str:
    if not database_url.startswith("sqlite"):
        return database_url

    sqlite_path = database_url.removeprefix("sqlite:///")
    if not sqlite_path or sqlite_path.startswith("/"):
        return database_url

    absolute_path = (BASE_DIR / sqlite_path).resolve()
    return f"sqlite:///{absolute_path.as_posix()}"


DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{(BASE_DIR / 'biblioteca.db').resolve().as_posix()}"
DATABASE_URL = _resolver_sqlite_url(DATABASE_URL)

engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True, **engine_kwargs)
SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)


class Base(DeclarativeBase):
    pass
