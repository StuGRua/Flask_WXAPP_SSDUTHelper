import os
import time
from typing import AbstractSet

from flask import Flask, jsonify, abort, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask('test')
# # 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:\\Project\\PY\\WX_backend\\model\\test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'user_info'
    userid = db.Column(db.BIGINT, primary_key=True)
    phonenumber = db.Column(db.BIGINT, unique=True)
    user_name = db.Column(db.String(32), default='NotSet')
    password_hash = db.Column(db.String(128), default='000000')
    major = db.Column(db.String(32), default='NotSet')
    grade = db.Column(db.String(32), default='NotSet')
    user_status = db.Column(db.String(32), default='OK')
    print('Building Done', type(userid), type(password_hash))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        print(self.password_hash)

    def verify_password(self, password):
        res = check_password_hash(self.password_hash, password)
        print(res)
        return res

    def generate_auth_token(self, expires_in=600):
        res = jwt.encode(payload={'id': self.userid, 'exp': time.time() + expires_in}, key=app.config['SECRET_KEY'],
                         algorithm='HS256')
        print(res, 'generated')
        return res

    @staticmethod
    def verify_auth_token(token):
        print('token?')
        try:
            print('token in:', token)
            data = jwt.decode(jwt=token, key=app.config['SECRET_KEY'], algorithms='HS256')
            print(data)
        except Exception as e:
            print(e)
            print('no token1')
            return
        return User.query.get(data['id'])

# 验证密码/token模块
@auth.verify_password
def verify_password(userid_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(userid_or_token)
    if not user:
        print('not token')
        # try to authenticate with username/password
        user = User.query.filter_by(userid=userid_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# class user_info(db.Model):
#     __tablename__ = 'user_info'
#     userid = db.Column(db.BIGINT, primary_key=True, nullable=False)
#     phonenumber = db.Column(BIGINT, primary_key=True, nullable=False)
#     user_name = db.Column(db.VARCHAR(255))
#     major = db.Column(db.VARCHAR(255))
#     grade = db.Column(db.VARCHAR(255))
#     user_status = db.Column(db.VARCHAR(255))
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
#
#
# class order_list(db.Model):
#     __tablename__ = 'order_list'
#     order_id = db.Column(db.VARCHAR(255), primary_key=True, nullable=False)
#     pub_id = db.Column(db.BIGINT, nullable=False)
#     rec_id = db.Column(db.BIGINT)
#     start_time = db.Column(db.DATETIME)
#     end_time = db.Column(db.DATETIME)
#     order_stat = db.Column(db.VARCHAR(255))
#     order_payment = db.Column(db.VARCHAR(255))
#     order_info = db.Column(db.VARCHAR(255))
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
#
#
# # 字符串转二进制
# def b_encode(s):
#     return (''.join([bin(ord(c)).replace('0b', '') for c in s]))
#
#
# # 二进制转字符串
# def b_decode(s):
#     return (''.join([chr(i) for i in [int(b, 2) for b in s.split('')]]))
#
#
# # 寻找用户是否存在
# def search_user(id):
#     result = user_info.query.filter_by(userid=id).first()
#     if result is None:
#         return (None)
#     else:
#         return (result.to_dict())
#
#
# # 插入新用户
# def insert_user(userid, phonenumber, user_name, major, grade, user_status):
#     engine = create_engine(
#         'mysql+mysqlconnector://StuG:x74rtw05@localhost:3306/wxapp')
#     metadata = MetaData(engine)
#     # 连接数据表
#     order_table = Table('user_info', metadata, autoload=True)
#     try:  # 创建 insert 对象
#         ins = order_table.insert()
#         # 绑定要插入的数据
#         ins = ins.values(userid=userid, phonenumber=phonenumber, user_name=user_name, major=major, grade=grade,
#                          user_status=user_status)
#         # 连接引擎
#         conn = engine.connect()
#         # 执行语句
#         result = conn.execute(ins)
#         return True
#     except:
#         print(result)
#         return (False)
#
#
# # 插入新订单
# def insert_order(order_id, pub_id, rec_id, start_time, end_time, order_stat, order_payment, order_info):
#     engine = create_engine(
#         'mysql+mysqlconnector://StuG:x74rtw05@localhost:3306/wxapp')
#     metadata = MetaData(engine)
#     # 连接数据表
#     order_table = Table('order_info', metadata, autoload=True)
#     try:  # 创建 insert 对象
#         ins = order_table.insert()
#         # 绑定要插入的数据
#         ins = ins.values(order_id=order_id, rec_id=rec_id, pub_id=pub_id, start_time=start_time, end_time=end_time,
#                          order_stat=order_stat, order_payment=order_payment,
#                          order_info=order_info)
#         # 连接引擎
#         conn = engine.connect()
#         # 执行语句
#         result = conn.execute(ins)
#         return True
#     except:
#         print(result)
#         return (False)
