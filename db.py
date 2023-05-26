import enum

from sqlalchemy import create_engine, Column, DateTime, func, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


SQLALCHEMY_DATABASE_URL = 'postgresql://trainee:trainee@localhost:5432/eora'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class AnswerTypeChoices(enum.Enum):
    positive = 'positive'
    negative = 'negative'


class PKModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)


class TimeStampedModel(Base):
    __abstract__ = True

    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())


class User(PKModel, TimeStampedModel, Base):
    __tablename__ = 'user'

    states = relationship('State', back_populates='user', order_by='State.id')


class State(PKModel, TimeStampedModel, Base):
    __tablename__ = 'state'

    step = Column(Integer)
    question = Column(String)
    answer_text = Column(String)
    answer_type = Column(Enum(AnswerTypeChoices))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='states')