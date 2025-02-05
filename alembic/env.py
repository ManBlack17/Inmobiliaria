from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base  # Importar los modelos
from app.database import DATABASE_URL
from sqlalchemy.sql import text

# Configuración del log de Alembic
config = context.config
fileConfig(config.config_file_name)

# Establecer la URL de la base de datos desde `database.py`
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configurar el esquema por defecto
SCHEMA_NAME = "inmobiliaria"

# Definir metadatos de los modelos
Base.metadata.schema = SCHEMA_NAME  # 📌 Asegurar que Alembic use el esquema correcto
target_metadata = Base.metadata


def run_migrations_offline():
    """Ejecuta las migraciones en modo offline."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta las migraciones en modo online con conexión a la base de datos."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # 📌 Establecer el esquema por defecto en la conexión
        connection.execute(text(f'SET search_path TO {SCHEMA_NAME}'))
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
