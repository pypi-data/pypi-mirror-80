from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker


def session_maker(config):
    engine = engine_from_config(config, prefix="db.", pool_pre_ping=True)

    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return session
