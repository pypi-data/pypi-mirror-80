# -*- coding: utf-8 -*-
'''data structure and useful utils'''

from jinja2 import Template

import json


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum

Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=False)
Session = sessionmaker(bind=engine)


class Data(Base):
    __tablename__ = 'users'

    chat_id       = Column(Integer, primary_key=True)
    step          = Column(String, default = 'not setted')

    @classmethod
    async def build(cls, event):
        return session.query(Data).filter_by(chat_id=event.chat_id).first() \
            or await Data.create_user(chat_id=event.chat_id)

    @classmethod
    async def create_user(cls, **kwargs):
        self = Data(**kwargs)
        session.add(self)
        session.commit()
        return self

    async def change_step(self, new_step):
        self.step = new_step
        session.add(self)
        session.commit()

    async def current_step(self):
        return self.step

try:
    session
except NameError:
    session = Session()

Base.metadata.create_all(engine)
