import logging
import json
import sqlalchemy as db
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import Token as token

with open('API/API.json', 'r') as file:
            api = json.load(file)

bot = Bot(token.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


engine = db.create_engine('sqlite:///db.sqlite')
connection = engine.connect()
metadata = db.MetaData()


main = db.Table('main', metadata,
                db.Column('Id', db.Integer(), primary_key=True),
                db.Column('Nickname', db.String(255), nullable=False),
                db.Column('Source', db.String(255), nullable=False, default='https://yande.re'),
                db.Column('Count', db.Integer(), nullable=False, default=1),
                )

metadata.create_all(engine)


def add_new_user(message):
    try:
        connection = engine.connect()
        query = db.insert(main).values(Id=message.from_user.id, Nickname=str(message.from_user.username))
        connection.execute(query)
    except:
        pass


def check_db():
    connection = engine.connect()
    results = connection.execute(db.select([main]))
    for row in results:
        print(row)


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
