from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float, DateTime



Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_designer = Column(Boolean, default=False)
    user_data_id = relationship("User_Data")
    tithe_user_id = relationship("Tithe", foreign_keys="Tithe.user_id")
    tithe_treasurer_id = relationship("Tithe", foreign_keys="Tithe.treasurer_id")
    finance_treasurer_id = relationship("Offers")
    access_user_id = relationship("Access")
    expenses_treasurer_id = relationship("Expenses")

    def __init__(self, name, email, hash, is_admin=False, is_designer=False):
        self.name = name
        self.email = email
        self.hash = hash
        self.is_admin = is_admin
        self.is_designer = is_designer

    def __repr__(self):
        return f'Pessoa({self.name})'


class User_Data(Base):
    __tablename__ = "user_data"
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True, nullable=False)
    cep = Column(String, nullable=False)
    address = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    birth = Column(Date, nullable=False)
    added = Column(Date)

    def __init__(self, user_id, cep, address, gender, tel, birth, added):
        self.user_id = user_id
        self.cep = cep
        self.address = address
        self.gender = gender
        self.tel = tel
        self.birth = birth
        self.added = added

class Tithe(Base):
    __tablename__ = "tithe"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    value = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    treasurer_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __init__(self, user_id, value, date, treasurer_id):
        self.user_id = user_id
        self.value = value
        self.date = date
        self.treasurer_id = treasurer_id

class Offers(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    value = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    treasurer_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __init__(self, value, date, treasurer_id):
        self.value = value
        self.date = date
        self.treasurer_id = treasurer_id

class Access(Base):
    __tablename__ = 'access'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    datetime = Column(DateTime, nullable=False)

    def __init__(self, user_id, datetime):
        self.user_id = user_id
        self.datetime = datetime

class Waiting_Approval(Base):
    __tablename__ = 'waiting_approval'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hash = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    address = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    birth = Column(Date, nullable=False)

    def __init__(self, name, email, hash, cep, address, gender, tel, birth):
        self.name = name
        self.email = email
        self.hash = hash
        self.cep = cep
        self.address = address
        self.gender = gender
        self.tel = tel
        self.birth = birth

class Expenses(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    value = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    treasurer_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __init__(self, value, description, date, treasurer_id):
        self.value = value
        self.description = description
        self.date = date
        self.treasurer_id = treasurer_id

class Finance(Base):
    __tablename__ = 'finance'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    entry = Column(Float, nullable=False)
    issues = Column(Float, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    period_balance = Column(Float, nullable=False)
    total_balance = Column(Float, nullable=False)

    def __init__(self, entry, issues, start, end, period_balance, total_balance):
        self.entry = entry
        self.issues = issues
        self.start = start
        self.end = end
        self.period_balance = period_balance
        self.total_balance = total_balance
