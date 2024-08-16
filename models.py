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
    birth_date = Column(DateTime, default='1987-09-09', nullable=False)
    phone = Column(String(50), nullable=False)
    funds = Column(Integer, default=0, nullable=False)

    def __init__(self, login, password, birth_date, phone):  #, funds):
        self.login = login
        self.password = password
        self.birth_date = birth_date
        self.phone = phone
        self.funds = 0

    # def __repr__(self): # приклад мабудь
    #     return f'<User {self.login!r}>'

    def add_funds(self, amount):
        if amount is not None and amount > 0:
            self.funds += amount

    def withdraw(self, amount):
        if amount is not None and amount > 0:
            new_funds = self.funds - amount
            self.funds = max(new_funds, 0)


class Coach(Base):
    __tablename__ = 'coach'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    age = Column(Integer, unique=True, nullable=False)
    sex = Column(String(50), unique=True, nullable=False)
    fitness_center_id = Column(Integer, ForeignKey('fitness_center.id'), nullable=False)


class CoachSchedule(Base):
    __tablename__ = 'coach_schedule'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    date = Column(String(50), nullable=False)
    coach_id = Column(Integer, ForeignKey('coach.id'), nullable=False)
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)


class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False)
    duration = Column(Integer, default=0, nullable=False)
    description = Column(String(50), nullable=False)
    price = Column(Integer, default=0, nullable=False)
    fitness_center_id = Column(Integer, ForeignKey('fitness_center.id'), nullable=False)
    max_attendees = Column(Integer, default=1, nullable=False)


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    coach_id = Column(Integer, ForeignKey('coach.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    date = Column(String(10), nullable=False)
    time = Column(String(10), nullable=False)


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    coach_id = Column(Integer, ForeignKey('coach.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    points = Column(Integer, default=0, nullable=False)
    text = Column(String(100), nullable=False)


class Resources(Base):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    amount = Column(Integer, default=0, nullable=False)
