# filepath: c:\Users\user\OneDrive\Desktop\diabetes_api\alembic\env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
import os

# Import all your models here
from app.models import Base  
from models.user_models import User
from app.models import PredictionLog

# Load environment variables
load_dotenv()

# this is the Alembic Config object
config = context.config

# Update the DATABASE_URL with SSL mode for Supabase
database_url = os.getenv("DATABASE_URL")
if database_url:
    # Add SSL mode and other connection parameters
    config.set_main_option(
        "sqlalchemy.url",
        f"{database_url}?sslmode=require"
    )

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()