from logging.config import fileConfig
import sys
from pathlib import Path

from alembic import context

# Add the project root to Python path so we can import our models
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after adding to path - import both Base and your engine
# No need for load_dotenv() here since models.py already does it
from src.dao.database_instance import Base, engine, DATABASE_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Set the database URL dynamically from your models.py
config.set_main_option("sqlalchemy.url", DATABASE_URL)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_run_migrations_offline__mutmut_orig() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_1() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = None
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_2() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=None,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_3() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=None,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_4() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=None,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_5() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts=None,
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_6() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_7() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_8() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_9() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_10() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=False,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_11() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"XXparamstyleXX": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_12() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"PARAMSTYLE": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_13() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "XXnamedXX"},
    )

    with context.begin_transaction():
        context.run_migrations()


def x_run_migrations_offline__mutmut_14() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL directly instead of going through config
    # (though config.get_main_option("sqlalchemy.url") would be the same value)
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "NAMED"},
    )

    with context.begin_transaction():
        context.run_migrations()

x_run_migrations_offline__mutmut_mutants : ClassVar[MutantDict] = {
'x_run_migrations_offline__mutmut_1': x_run_migrations_offline__mutmut_1, 
    'x_run_migrations_offline__mutmut_2': x_run_migrations_offline__mutmut_2, 
    'x_run_migrations_offline__mutmut_3': x_run_migrations_offline__mutmut_3, 
    'x_run_migrations_offline__mutmut_4': x_run_migrations_offline__mutmut_4, 
    'x_run_migrations_offline__mutmut_5': x_run_migrations_offline__mutmut_5, 
    'x_run_migrations_offline__mutmut_6': x_run_migrations_offline__mutmut_6, 
    'x_run_migrations_offline__mutmut_7': x_run_migrations_offline__mutmut_7, 
    'x_run_migrations_offline__mutmut_8': x_run_migrations_offline__mutmut_8, 
    'x_run_migrations_offline__mutmut_9': x_run_migrations_offline__mutmut_9, 
    'x_run_migrations_offline__mutmut_10': x_run_migrations_offline__mutmut_10, 
    'x_run_migrations_offline__mutmut_11': x_run_migrations_offline__mutmut_11, 
    'x_run_migrations_offline__mutmut_12': x_run_migrations_offline__mutmut_12, 
    'x_run_migrations_offline__mutmut_13': x_run_migrations_offline__mutmut_13, 
    'x_run_migrations_offline__mutmut_14': x_run_migrations_offline__mutmut_14
}

def run_migrations_offline(*args, **kwargs):
    result = _mutmut_trampoline(x_run_migrations_offline__mutmut_orig, x_run_migrations_offline__mutmut_mutants, args, kwargs)
    return result 

run_migrations_offline.__signature__ = _mutmut_signature(x_run_migrations_offline__mutmut_orig)
x_run_migrations_offline__mutmut_orig.__name__ = 'x_run_migrations_offline'


def x_run_migrations_online__mutmut_orig() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def x_run_migrations_online__mutmut_1() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = None

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def x_run_migrations_online__mutmut_2() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=None, target_metadata=target_metadata, render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def x_run_migrations_online__mutmut_3() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=None, render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def x_run_migrations_online__mutmut_4() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, render_as_batch=None,
        )

        with context.begin_transaction():
            context.run_migrations()


def x_run_migrations_online__mutmut_5() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            target_metadata=target_metadata, render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def x_run_migrations_online__mutmut_6() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def x_run_migrations_online__mutmut_7() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, )

        with context.begin_transaction():
            context.run_migrations()


def x_run_migrations_online__mutmut_8() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use your engine from models.py instead of creating a new one
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, render_as_batch=False,
        )

        with context.begin_transaction():
            context.run_migrations()

x_run_migrations_online__mutmut_mutants : ClassVar[MutantDict] = {
'x_run_migrations_online__mutmut_1': x_run_migrations_online__mutmut_1, 
    'x_run_migrations_online__mutmut_2': x_run_migrations_online__mutmut_2, 
    'x_run_migrations_online__mutmut_3': x_run_migrations_online__mutmut_3, 
    'x_run_migrations_online__mutmut_4': x_run_migrations_online__mutmut_4, 
    'x_run_migrations_online__mutmut_5': x_run_migrations_online__mutmut_5, 
    'x_run_migrations_online__mutmut_6': x_run_migrations_online__mutmut_6, 
    'x_run_migrations_online__mutmut_7': x_run_migrations_online__mutmut_7, 
    'x_run_migrations_online__mutmut_8': x_run_migrations_online__mutmut_8
}

def run_migrations_online(*args, **kwargs):
    result = _mutmut_trampoline(x_run_migrations_online__mutmut_orig, x_run_migrations_online__mutmut_mutants, args, kwargs)
    return result 

run_migrations_online.__signature__ = _mutmut_signature(x_run_migrations_online__mutmut_orig)
x_run_migrations_online__mutmut_orig.__name__ = 'x_run_migrations_online'


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
