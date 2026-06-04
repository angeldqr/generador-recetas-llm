from pathlib import Path
import sys

from sqlalchemy.exc import OperationalError

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import Base, engine
from app.models import Ingredient, Rating, Recipe, User  # noqa: F401


def main() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except (OperationalError, UnicodeDecodeError) as error:
        raise SystemExit(
            "No se pudo conectar a PostgreSQL. Revisa DATABASE_URL y "
            "POSTGRES_PASSWORD en .env antes de crear las tablas."
        ) from error

    table_names = ", ".join(sorted(Base.metadata.tables.keys()))
    print(f"Tablas creadas/verificadas: {table_names}")


if __name__ == "__main__":
    main()
