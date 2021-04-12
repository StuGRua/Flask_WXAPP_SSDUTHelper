import datetime

from flask import jsonify, abort, request
from flask import url_for

from model.model import *


# WX_APPID = 'wx933173854a5a9ba2'
# WX_SECRET = 'ebf07d30198d42d3322fcbc82c996f9e'


# 具体导入配
# 根据需求导入仅供参考
@app.route('/api/what', methods=['GET'])
def what_info():
    return "无内鬼"


@app.route('/api/users', methods=['POST'])
def new_user():
    print(request.json)
    rqjson = request.json
    userid = rqjson.get('userid')
    phonenumber = rqjson.get('phonenumber')
    password = rqjson.get('password')
    user_name = rqjson.get('user_name')
    major = rqjson.get('major')
    grade = rqjson.get('grade')
    if userid is None or password is None or phonenumber is None:
        abort(400)  # missing arguments
    if User.query.filter_by(userid=userid).first() is not None or User.query.filter_by(
            phonenumber=phonenumber).first() is not None:
        abort(400)  # existing user
    user = User(userid=userid, phonenumber=phonenumber, user_name=user_name, major=major, grade=grade)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'userid': user.userid}), 201,
            {'Location': url_for('get_user', id=user.userid, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'userid': user.userid, 'username': user.user_name})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token, 'duration': 600, 'user_name': g.user.user_name})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.userid})


@app.route('/api/all_undo_order')
@auth.login_required
def all_undo_order():
    pre_res = db.session.query(Order).filter(Order.order_stat == '未接受').all()
    res = OrderToDict(pre_res)
    return jsonify(res), 201


@app.route('/api/my_order_pub')
@auth.login_required
def my_order_pub():
    res = Order.query.filter_by(pub_id=g.user.userid).all()
    res = OrderToDict(res)
    return jsonify(res), 201


@app.route('/api/my_order_recv')
@auth.login_required
def my_order_recv():
    res = Order.query.filter_by(rec_id=g.user.userid)
    res = OrderToDict(res)
    return jsonify(res), 201


@app.route('/api/publish_order', methods=['POST'])
@auth.login_required
def publish_order():
    rqjson = request.json
    print(rqjson)
    order_title = rqjson.get('order_title')
    pub_id = g.user.userid
    # rec_id=rqjson.get('rec_id')
    start_time = datetime.datetime.strptime(rqjson.get('start_time'), '%Y-%m-%d %H:%M')
    end_time = datetime.datetime.strptime(rqjson.get('end_time'), '%Y-%m-%d %H:%M')
    order_payment = rqjson.get('order_payment')
    order_info = rqjson.get('order_info')

    if order_title is None or pub_id is None or order_payment is None:
        abort(400)  # missing arguments
    if User.query.filter_by(userid=pub_id).first() is None:
        abort(400)  # no existing user
    order = Order(order_title=order_title, pub_id=pub_id, start_time=start_time, end_time=end_time,
                  order_payment=order_payment, order_info=order_info)
    db.session.add(order)
    db.session.commit()
    return (jsonify({'order_id': order.order_id, 'order_name': order.order_title}), 201,
            {'Location': url_for('get_user', id=g.user.userid, _external=True)})


@app.route('/api/get_order', methods=['POST'])
@auth.login_required
def get_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    if order_id is None:
        abort(400)  # missing arguments
    if Order.query.filter_by(order_id=order_id).first() is None:
        abort(400)  # no existing user
    db.session.query(Order).filter(Order.order_id == order_id). \
        update({"order_stat": '正在进行', "rec_id": g.user.userid})
    return jsonify({'order_id': order_id, "order_stat": '正在进行'}), 201


@app.route('/api/finish_order', methods=['POST'])
@auth.login_required
def finish_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    if order_id is None:
        abort(400)  # missing arguments
    if Order.query.filter_by(order_id=order_id, pub_id=g.user.userid).first() is None:
        abort(400)  # no existing user
    db.session.query(Order).filter(Order.order_id == order_id). \
        update({"order_stat": '已完成'})
    return jsonify({'order_id': order_id, "order_stat": '正在进行'}), 201


@app.route('/api/del_order', methods=['POST'])
@auth.login_required
def del_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    if order_id is None:
        abort(400)  # missing arguments
    pre_del = db.session.query(Order).filter(Order.order_id == order_id).first()
    if pre_del is None:
        abort(400)  # no existing user
    db.session.delete(pre_del)
    db.session.commit()
    return jsonify({'order_id': order_id, "order_stat": '正在进行'}), 201


@app.route('/api/modify_order', methods=['POST'])
@auth.login_required
def modify_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    order_title = rqjson.get('order_title')
    pub_id = g.user.userid
    # rec_id=rqjson.get('rec_id')
    start_time = datetime.datetime.strptime(rqjson.get('start_time'), '%Y-%m-%d')
    end_time = datetime.datetime.strptime(rqjson.get('end_time'), '%Y-%m-%d')
    order_payment = rqjson.get('order_payment')
    order_info = rqjson.get('order_info')

    if order_title is None or pub_id is None or order_payment is None:
        abort(400)  # missing arguments
    pre_fix = db.session.query(Order).filter(Order.pub_id == pub_id, Order.order_id == order_id).first()
    if pre_fix is None:
        abort(400)  # no existing user
    pre_fix.update(
        {'order_title': order_title, 'start_time': start_time, 'end_time': end_time, 'order_payment': order_payment,
         'order_info': order_info})
    db.session.commit()
    return (jsonify({'order_id': order_id}), 201,
            {'Location': url_for('get_user', id=g.user.userid, _external=True)})


def SimpleOrderToDict(pre_res):
    if not pre_res:
        return
    res = []
    for x in pre_res:
        temp = {
            'order_id': x.order_id,
            'order_title': x.order_title,
            'pub_id': x.pub_id,
            'start_time': x.start_time,
            'end_time': x.end_time,
            'order_stat': x.order_stat,
            'order_payment': x.order_payment,
        }
        res.append(temp)
    return res


def OrderToDict(pre_res):
    if not pre_res:
        return
    res = []
    for x in pre_res:
        temp = {
            'order_id': x.order_id,
            'order_title': x.order_title,
            'pub_id': x.pub_id,
            'rec_id': x.rec_id,
            'start_time': x.start_time,
            'end_time': x.end_time,
            'order_stat': x.order_stat,
            'order_payment': x.order_payment,
            'order_info': x.order_info
        }
        res.append(temp)
    return res


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

# curl -H "Content-Type:application/json" -H "Data_Type:msg" -X POST --data "{\"username\":\"xxx\",password:\"1233423\"}" http://127.0.0.1:5000/api/users
