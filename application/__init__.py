from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI

#初始化数据库连接
engine = create_engine(SQLALCHEMY_DATABASE_URI)
#创建对象的基类
Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

app = Flask(__name__)

from .view import *
from .model import *
from .parent_line import *