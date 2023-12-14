from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import dotenv_values

config = dotenv_values(".env")
DB_USER=config.get("DB_USER")
DB_PASSWORD=config.get("DB_PASSWORD")
DB_HOST=config.get("DB_HOST")
DB_NAME=config.get("DB_NAME")

print(config.get("DB_HOST"))
engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}',
    echo=True
)

Base = declarative_base()
Session = sessionmaker()
