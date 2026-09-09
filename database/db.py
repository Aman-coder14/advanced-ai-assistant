from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine

from database.models import Base


_engine: Engine | None = None


def _get_database_url() -> str:
    """Read the database URL from Streamlit Cloud or the local environment."""
    database_url = str(st.secrets.get("DATABASE_URL", "")).strip()
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured in Streamlit Secrets."
        )

    if database_url.startswith("postgres://"):
        database_url = "postgresql+psycopg2://" + database_url[len("postgres://") :]
    elif database_url.startswith("postgresql://"):
        database_url = "postgresql+psycopg2://" + database_url[len("postgresql://") :]
    return database_url


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(
            _get_database_url(),
            pool_pre_ping=True,
            pool_recycle=1800,
        )
    return _engine


@contextmanager
def get_connection() -> Iterator[Connection]:
    """Yield a transactional SQLAlchemy connection."""
    with get_engine().begin() as connection:
        yield connection


def init_db() -> None:
    """Create the PostgreSQL schema when the app starts."""
    try:
        engine = get_engine()
        Base.metadata.create_all(engine)
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS "
                    "password_hash VARCHAR(255)"
                )
            )
    except Exception as error:
        st.error(f"Critical Database Initialization Error: {error}")
        raise
