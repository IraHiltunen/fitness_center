from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# engine = create_engine('sqlite:///db') # перевірити розширення db.db типу нема у мене розширення
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))

#engine = create_engine('sqlite:///db3')
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))

DB_STRING = 'postgresql+psycopg2://postgres:example@localhost:5432'
#DB_STRING = f'postgresql+psycopg2://postgres:example@{os.environ.get("DB_HOST", "localhost")}:5432'

engine = create_engine(DB_STRING)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# DB_STRING_TEMPLATE = 'postgresql+psycopg2://{0}:{1}@{2}:5432' #  це для постгрес
# DB_STRING = DB_STRING_TEMPLATE.format(os.environ.get('POSTGRES_USER'),# так краще з паролями працювати
#                                       os.environ.get('POSTGRES_PASSWORD'),
#                                       os.environ.get('DB_HOST', 'localhost'))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)