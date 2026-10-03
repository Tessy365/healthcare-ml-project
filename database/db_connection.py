import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Default to local PostgreSQL or fallback URI
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/healthcare_db",
)

# Ensure SQLAlchemy explicitly uses the psycopg2 driver
if DATABASE_URL.startswith("postgres://"):
  DATABASE_URL = DATABASE_URL.replace(
      "postgres://", "postgresql+psycopg2://", 1
  )
elif DATABASE_URL.startswith(
    "postgresql://"
) and not DATABASE_URL.startswith("postgresql+"):
  DATABASE_URL = DATABASE_URL.replace(
      "postgresql://", "postgresql+psycopg2://", 1
  )

# Create SQLAlchemy Database Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
  """Yields a database session for API endpoints or scripts."""
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()