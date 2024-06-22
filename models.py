from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base


class FitnessCenter(Base):
    __tablename__ = 'fitness_center'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    address = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    contacts = Column(String(50), unique=False, nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    birth_date = Column(String(50), default='1987-09-09', nullable=False)
    phone = Column(String(50), nullable=False)
    funds = Column(Integer, default=0, nullable=False)

    def __init__(self, login, password, birth_date, phone, funds):
        self.login = login
        self.password = password
        self.birth_date = birth_date
        self.phone = phone
        self.funds = 0

    def add_funds(self, amount):
        if amount is not None and amount > 0:
            self.funds += amount

    def withdraw(self, amount):
        if amount is not None and amount > 0:
            new_funds = self.funds - amount
            self.funds = max(max)

