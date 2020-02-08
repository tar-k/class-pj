from sqlalchemy import (Column, String, Text, Integer, Date, Boolean, ForeignKey, create_engine)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    registered_on = Column(Date, default=datetime.date.today())

    tasks = relationship('Task')

    def __str__(self):
        return '\n'.join([self.id, self.name, self.password, self.email, self.registered_on])

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(20), nullable=False)
    description = Column(Text)
    created_on = Column(Date, default=datetime.date.today())
    deadline = Column(Date)
    status = Column(Boolean, default=0)

    author= relationship('User')

    def __str__(self):
        return '\n'.join([self.id, 
                            self.user_id, 
                            self.title, 
                            self.password, 
                            self.description, 
                            self.created_on, 
                            self.deadline, 
                            self.status])

Base.metadata.create_all()

def add_user(name, email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind = engine)
    session.add(User(name=name, email=email, password=password))
    session.commit()
    session.close()

def check_user(email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind = engine)
    user = session.query(User).filter_by(email=email, password=password).first()
    session.close()
    return user

def add_task(user, title, details, deadline_date):
    engine = create_engine('sqlite:///app.db', echo=True)
    db_session = Session(bind = engine)


    db_user = db_session.query(User).filter_by(name=user).first()
    if deadline_date:
        deadline_date = datetime.date.fromisoformat(deadline_date)
    else:
        deadline_date = None
    db_user.tasks.append(Task(title=title,
                            description=details,
                            deadline=deadline_date))
    #session.add(Task(title=title, description=details, deadline=deadline_date))
    db_session.commit()
    db_session.close()

def get_user_tasks(name):
    engine = create_engine('sqlite:///app.db', echo=True)
    db_session = Session(bind = engine)
    db_user = db_session.query(User).filter_by(name=name).first()
    user_tasks = db_user.tasks  
    db_session.close
    return user_tasks