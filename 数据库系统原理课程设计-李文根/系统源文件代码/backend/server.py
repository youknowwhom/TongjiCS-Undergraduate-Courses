import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from functools import wraps
from datetime import datetime, timedelta
from util import getLocalTimeString

db = SQLAlchemy()
app = Flask(__name__, static_url_path='')
app.secret_key = '#iLoveDataBase'
app.config['JWT_SECRET_KEY'] = '#iLoveDataBase'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///typhoon.db"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)
CORS(app)

db.init_app(app)

jwt = JWTManager()
jwt.init_app(app)


"""
以下为数据库表设计
"""
class RegularUser(db.Model):
    __tablename__ = 'regular_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    district_id = db.Column(db.String(10), db.ForeignKey('district.id'))
    birthday = db.Column(db.DateTime)
    gender = db.Column(db.String(1))
    phone = db.Column(db.String(15))

    def __repr__(self):
        return f"<Regular User({self.id}): {self.name}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'district_id': self.district_id,
            'birthday': self.birthday,
            'gender': self.gender,
            'gender_literal': '男' if self.gender != 'F' else '女',
            'phone': self.phone
        }


class StationUser(db.Model):
    __tablename__ = 'station_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __repr__(self):
        return f"<Station User({self.id}): {self.name}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'longitude': self.longitude,
            'latitude': self.latitude
        }

    
class Typhoon(db.Model):
    __tablename__ = 'typhoon'

    id = db.Column(db.Integer, primary_key=True)
    chinese_id = db.Column(db.Integer)
    name = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    max_category = db.Column(db.Integer)
    max_wind_speed = db.Column(db.Float)
    min_pressure = db.Column(db.Float)

    def __repr__(self):
        return f"<Typhoon({self.id}): {self.name}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_time': getLocalTimeString(self.start_time),
            'end_time': getLocalTimeString(self.end_time) if self.end_time else '至今',
            'max_category': self.max_category
        }


class TyphoonPath(db.Model):
    __tablename__ = 'typhoon_path'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typhoon_id = db.Column(db.Integer, db.ForeignKey('typhoon.id'))
    station_id = db.Column(db.Integer, db.ForeignKey('station_user.id'))
    time = db.Column(db.DateTime)
    category = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    pressure = db.Column(db.Float)

    typhoon = db.relationship('Typhoon', backref=db.backref('paths'))

    def __repr__(self):
        return f"<TyphoonPath(typhoon_id={self.typhoon_id}, station_id={self.station_id}, time={self.time})>"


class TyphoonWarning(db.Model):
    __tablename__ = 'typhoon_warning'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typhoon_id = db.Column(db.Integer, db.ForeignKey('typhoon.id'))
    station_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    level = db.Column(db.String(10))

    def __repr__(self):
        return f"<TyphoonWarning(typhoon_id={self.typhoon_id}, station_id={self.station_id}, time={self.time})>"


class District(db.Model):
    __tablename__ = 'district'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    population = db.Column(db.Integer)
    father_id = db.Column(db.String(10), db.ForeignKey('district.id'))


class Satellite(db.Model):
    __tablename__ = 'satellite'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    launch_date = db.Column(db.DateTime)
    type = db.Column(db.String(50))
    current_longtitude = db.Column(db.Float)
    current_latitude = db.Column(db.Float)

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'launch_date': getLocalTimeString(self.launch_date),
            'type': self.type,
            'current_longtitude': self.current_longtitude,
            'current_latitude': self.current_latitude
        }


class Subscribe(db.Model):
    __tablename__ = 'subscribe'
    user_id = db.Column(db.Integer, db.ForeignKey('station_user.id'), primary_key=True)
    typhoon_id = db.Column(db.Integer, db.ForeignKey('typhoon.id'), primary_key=True)


class Connect(db.Model):
    __tablename__ = 'connect'
    station_id = db.Column(db.Integer, db.ForeignKey('station_user.id'), primary_key=True)
    satellite_id = db.Column(db.Integer, db.ForeignKey('satellite.id'), primary_key=True)
    

class Monitor(db.Model):
    __tablename__ = 'monitor'
    user_id = db.Column(db.Integer, db.ForeignKey('regular_user.id'), primary_key=True)
    district_id = db.Column(db.String(10), db.ForeignKey('district.id'), primary_key=True)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('regular_user.id'))
    path_id = db.Column(db.Integer, db.ForeignKey('typhoon_path.id'))
    checked = db.Column(db.Boolean, default=False)


class Alert(db.Model):
    __tablename__ = 'alert'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('regular_user.id'))
    warning_id = db.Column(db.Integer, db.ForeignKey('typhoon_warning.id'))


with app.app_context(): 
    db.create_all()




"""
以下为各个API
"""

# 获取所有台风信息
@app.route('/getAllTyphoons')
@jwt_required()
def get_all_typhoons():
    result = Typhoon.query.all()
    typhoon_data = [{'id': row.id, 'name': row.name, 'start_time': row.start_time, 'end_time': row.end_time, 'max_category': row.max_category, 'max_wind_speed': row.max_wind_speed, 'min_pressure': row.min_pressure} for row in result]
    return jsonify({'typhoon': typhoon_data})


# 根据ID获取指定台风信息
@app.route('/getTyphoonById/<int:typhoon_id>')
@jwt_required()
def get_typhoon(typhoon_id):
    result = Typhoon.query.filter_by(id=typhoon_id).first()
    typhoon_data = {'id': result.id, 'name': result.name, 'start_time': result.start_time, 'end_time': result.end_time, 'max_category': result.max_category, 'max_wind_speed': result.max_wind_speed, 'min_pressure': result.min_pressure}
    return jsonify({'typhoon': typhoon_data})


# 根据ID获取指定台风的路径信息
@app.route('/getTyphoonPathById/<int:typhoon_id>')
@jwt_required()
def get_typhoon_path(typhoon_id):
    result = TyphoonPath.query.filter_by(typhoon_id=typhoon_id).all()
    path_data = [{'station_id': row.station_id, 'time': row.time, 'category': row.category, 'latitude': row.latitude, 'longitude': row.longitude, 'wind_speed': row.wind_speed, 'pressure': row.pressure} for row in result]
    return jsonify({'path': path_data})

# 根据字符串搜索台风信息
@app.route('/searchTyphoonByStr/<string:str>')
@jwt_required(optional=True)
def searchTyphoonByStr(str):
    results = Typhoon.query.filter(Typhoon.name.ilike(f'%{str}%')).all()
    typhoon_data = [{'id': row.id, 'name': row.name, 'start_time': row.start_time} for row in results]
    return jsonify({'typhoon': typhoon_data})

# 根据字符串搜索未消亡的台风信息
@app.route('/searchNotEndedTyphoonByStr/<string:str>')
@jwt_required(optional=True)
def searchNotEndedTyphoonByStr(str):
    results = Typhoon.query.filter(
        Typhoon.name.ilike(f'%{str}%'),
        Typhoon.end_time == None  # 检查end_time是否为null
    ).all()
    typhoon_data = [{'id': row.id, 'name': row.name, 'start_time': row.start_time} for row in results]
    return jsonify({'typhoon': typhoon_data})

# 创建台风
@app.route('/createTyphoon', methods=['POST'])
@jwt_required()
def createTyphoon():
    json = request.get_json()
    if not json['name'] or json['longitude'] == None or json['latitude'] == None \
        or not json['time'] or json['category'] == None or json['wind_speed'] == None:
        return jsonify({'error': '台风信息不完整！'}), 403
    
    time = datetime.strptime(json['time'], '%Y-%m-%dT%H:%M:%S.%fZ')

    typhoon = Typhoon(name=json['name'], start_time=time, max_category=json['category'],
                      max_wind_speed=json['wind_speed'], min_pressure=json['pressure'])
    db.session.add(typhoon)
    db.session.commit()

    station_id = get_jwt_identity()['id']
    path = TyphoonPath(typhoon_id=typhoon.id, station_id=station_id, time=time, category=json['category'],
                                  latitude=json['latitude'], longitude=json['longitude'], wind_speed=json['wind_speed'], pressure=json['pressure'])
    db.session.add(path)
    db.session.commit()
    return jsonify({}), 200

# 消亡台风
@app.route('/endTyphoon/<int:typhoon_id>', methods=['POST'])
@jwt_required()
def endTyphoon(typhoon_id):
    path = TyphoonPath.query.filter_by(typhoon_id=typhoon_id).order_by(TyphoonPath.time.desc()).first()
    typhoon = Typhoon.query.filter_by(id=typhoon_id).first()
    typhoon.end_time = path.time
    db.session.commit()
    return jsonify({}), 200

# 创建台风路径
@app.route('/createTyphoonPath/<int:typhoon_id>', methods=['POST'])
@jwt_required()
def createTyphoonPath(typhoon_id):
    json = request.get_json()
    time = datetime.strptime(json['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    station_id = get_jwt_identity()['id']

    pathes = TyphoonPath.query.filter_by(typhoon_id=typhoon_id).all()
    for p in pathes:
        if p.time >= time:
            return jsonify({'error': '本次台风路径更新时间早于上次更新！'}), 403

    path = TyphoonPath(typhoon_id=typhoon_id, station_id=station_id, time=time, category=json['category'],
                                  latitude=json['latitude'], longitude=json['longitude'], wind_speed=json['wind_speed'], pressure=json['pressure'])
    
    # 下面更新最大风速、最低气压和最高级数信息
    typhoon = Typhoon.query.filter_by(id=typhoon_id).first()
    if typhoon.max_category < json['category']:
        typhoon.max_category = json['category']
    if typhoon.max_wind_speed < json['wind_speed']:
        typhoon.max_wind_speed = json['wind_speed']
    if typhoon.min_pressure > json['pressure']:
        typhoon.min_pressure = json['pressure']
    
    db.session.add(path)
    db.session.commit()

    # 下面更新台风路径消息
    users = db.session.query(Subscribe.user_id).filter_by(typhoon_id=typhoon_id).all()
    for user in users:
        message = Message(user_id=user[0], path_id=path.id)
        db.session.add(message)
    db.session.commit()

    return jsonify({}), 200


# 获取收藏台风列表
@app.route('/getAllTyphoonFav')
@jwt_required()
def get_all_typhoon_favorite():
    identity = get_jwt_identity()
    ans = Subscribe.query.filter_by(user_id=identity['id']).all()
    ans = [Typhoon.query.filter_by(id=subscribe.typhoon_id).first().serialize() for subscribe in ans]
    return ans, 200


# 判断当前台风是否收藏
@app.route('/getTyphoonFav/<int:typhoon_id>')
@jwt_required()
def get_typhoon_favorite(typhoon_id):
    identity = get_jwt_identity()
    id = identity['id']
    
    if Subscribe.query.filter_by(user_id=id, typhoon_id=typhoon_id).first():
        return jsonify({'star': True}), 200
    else:
        return jsonify({'star': False}), 200


# 台风加入收藏
@app.route('/setTyphoonFav/<int:typhoon_id>')
@jwt_required()
def set_typhoon_favorite(typhoon_id):
    identity = get_jwt_identity()
    id = identity['id']
    
    sub = Subscribe(user_id=id, typhoon_id=typhoon_id)
    db.session.add(sub)
    db.session.commit()
    return jsonify({}), 200


# 台风取消收藏
@app.route('/unsetTyphoonFav/<int:typhoon_id>')
@jwt_required()
def unset_typhoon_favorite(typhoon_id):
    identity = get_jwt_identity()
    id = identity['id']
    sub = Subscribe.query.filter_by(user_id=id, typhoon_id=typhoon_id).first()
    if not sub:
        return jsonify({}), 400
    else:
        db.session.delete(sub)
        db.session.commit()
        return jsonify({}), 200
    
# 创建预警信息
@app.route('/createAlert', methods=['POST'])
@jwt_required()
def createAlert():
    identity = get_jwt_identity()
    station_id = identity['id']
    json = request.get_json()
    warning = TyphoonWarning(station_id=station_id, typhoon_id=json['typhoon_id'], 
                             time=datetime.strptime(json['time'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                             level=json['level'])
    db.session.add(warning)
    db.session.commit()

    # 填写用户和预警的对应关系
    district_ids = db.session.query(Monitor.district_id).filter_by(user_id=station_id).all()
    user_ids = set()
    for district_id in district_ids:
        for uid in db.session.query(RegularUser.id).filter_by(district_id=district_id[0]).all():
            user_ids.update(uid)
    for id in user_ids:
        alert = Alert(user_id=id, warning_id=warning.id)
        db.session.add(alert)
    db.session.commit()

    return jsonify({}), 200

# 获取预警信息
@app.route('/getAlert')
@jwt_required()
def getAlert():
    identity = get_jwt_identity()
    user_id = identity['id']
    alerts = Alert.query.filter_by(user_id=user_id).all()
    ret = []

    for alert in alerts:
        warning = TyphoonWarning.query.filter_by(id=alert.warning_id).first()
        station = StationUser.query.filter_by(id=warning.station_id).first()
        ret.append({'station':station.name, 'time':warning.time, 'level':warning.level})
        db.session.delete(alert)

    db.session.commit()

    return jsonify({'info': ret}), 200

# 获取未读消息数量
@app.route('/getUnreadMessageNum')
@jwt_required()
def getUnreadMessageNum():
    identity = get_jwt_identity()
    user_id = identity['id']
    num = Message.query.filter_by(user_id=user_id, checked=False).count()
    return jsonify({'num': num}), 200


# 获取所有消息
@app.route('/getMessage')
@jwt_required()
def getMessage():
    identity = get_jwt_identity()
    user_id = identity['id']
    messages = Message.query.filter_by(user_id=user_id).all()

    ret = []
    for message in reversed(messages):
        path = TyphoonPath.query.filter_by(id=message.path_id).first()
        station = StationUser.query.filter_by(id=path.station_id).first()
        typhoon = Typhoon.query.filter_by(id=path.typhoon_id).first()
        time = getLocalTimeString(path.time)

        ret.append({'id':message.id, 'time':time, 'category':path.category, 
                    'longitude':path.longitude, 'latitude':path.latitude,
                    'pressure':path.pressure, 'wind_speed':path.wind_speed,
                    'station': station.name, 'typhoon': typhoon.name, 'checked':message.checked})
        message.checked = True

    return jsonify(ret), 200


# 已读消息
@app.route('/setMessageRead/<int:message_id>')
@jwt_required()
def setMessageRead(message_id):
    message = Message.query.filter_by(id=message_id).first()
    if message == None:
        return jsonify({'error': '消息不存在！'}), 400
    message.checked = True
    db.session.commit()

    return jsonify(), 200

# 创建卫星
@app.route('/createSatellite', methods=['POST'])
@jwt_required()
def createSatellite():
    json = request.get_json()
    if json['name'] == None or json['time'] == None or json['category'] == None \
        or json['longitude'] == None or json['latitude'] == None:
        return jsonify({'error': '卫星信息不完整！'}), 403
    
    satellite = Satellite(name = json['name'], launch_date = datetime.strptime(json['time'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                               type = json['category'], current_longtitude = json['longitude'], current_latitude = json['latitude'])
    db.session.add(satellite)
    db.session.commit()
    return jsonify({}), 200

# 根据字符串搜索卫星信息
@app.route('/searchSatelliteByStr/<string:str>')
@jwt_required()
def searchSatelliteByStr(str):
    results = Satellite.query.filter(
        Satellite.name.ilike(f'%{str}%'),
    ).all()
    satellite_data = [satellite.serialize() for satellite in results]
    return jsonify({'satellite': satellite_data})

# 创建卫星订阅
@app.route('/createSatelliteConnect/<int:satellite_id>', methods=['POST'])
@jwt_required()
def createSatelliteConnect(satellite_id):
    identity = get_jwt_identity()
    station_id = identity['id']
    if Connect.query.filter_by(station_id=station_id, satellite_id=satellite_id).first() != None:
        return jsonify({'error': '已订阅该卫星！'}), 403
    connect = Connect(station_id=station_id, satellite_id=satellite_id)
    db.session.add(connect)
    db.session.commit()
    return jsonify({}), 200

# 获取卫星订阅
@app.route('/getSatelliteConnect')
@jwt_required()
def getSatelliteConnect():
    identity = get_jwt_identity()
    station_id = identity['id']
    connects = Connect.query.filter_by(station_id=station_id).all()
    satellites = []
    for connect in connects:
        satellite = Satellite.query.filter_by(id=connect.satellite_id).first()
        satellites.append(satellite.serialize())
    return jsonify(satellites), 200

# 取消卫星订阅
@app.route('/cancelSatelliteConnect/<int:satellite_id>', methods=['POST'])
@jwt_required()
def cancelSatelliteConnect(satellite_id):
    identity = get_jwt_identity()
    station_id = identity['id']
    connect = Connect.query.filter_by(station_id=station_id, satellite_id=satellite_id).first()
    if not connect:
        return jsonify({'error': '未订阅该卫星！'}), 403
    db.session.delete(connect)
    db.session.commit()
    return jsonify({}), 200

"""
以下为身份管理
"""
# 普通用户注册
@app.route('/signup/regular', methods=['POST'])
def regularUserSignUp():
    json = request.get_json()
    if 'name' not in json or 'password' not in json \
        or json['name']=='' or json['password']=='':
        return jsonify({'error': '用户信息不完整！'}), 403
    user = RegularUser.query.filter_by(name = json['name']).first()
    if user != None:
        return jsonify({'error': '用户名已存在！'}), 403
    password = generate_password_hash(json['password'])
    user = RegularUser(name = json['name'], password = password, 
                       birthday = datetime.strptime(json['birthday'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                       gender = json['gender'], phone = json['phone'], district_id = json['district'])
    db.session.add(user)
    db.session.commit()
    return jsonify({}), 200

# 气象站用户注册
@app.route('/signup/station', methods=['POST'])
def stationUserSignUp():
    json = request.get_json()
    if 'name' not in json or 'password' not in json \
        or json['name']=='' or json['password']=='':
        return jsonify({'error': '用户信息不完整！'}), 403
    user = StationUser.query.filter_by(name = json['name']).first()
    if user != None:
        return jsonify({'error': '用户名已存在！'}), 403
    password = generate_password_hash(json['password'])
    user = StationUser(name = json['name'], password = password, 
                       longitude = json['longitude'], latitude = json['latitude'])
    db.session.add(user)
    db.session.commit()

    for district in json['district']:
        monitor = Monitor(user_id=user.id, district_id=district)
        db.session.add(monitor)
    db.session.commit()

    return jsonify({}), 200

# 普通用户登录
@app.route('/login/regular', methods=['POST'])
def regularUserLogin():
    json = request.get_json()
    user = RegularUser.query.filter_by(name = json['name']).first()
    if user == None:
        return jsonify({'error': '用户不存在！'}), 403
    if check_password_hash(user.password, json['password']):
        token = create_access_token(identity={'id':user.id, 'role':'regular'})
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': '密码错误！'}), 403
    
# 气象站登录
@app.route('/login/station', methods=['POST'])
def stationUserLogin():
    json = request.get_json()
    user = StationUser.query.filter_by(name = json['name']).first()
    if user == None:
        return jsonify({'error': '用户不存在！'}), 403
    if check_password_hash(user.password, json['password']):
        token = create_access_token(identity={'id':user.id, 'role':'station'})
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': '密码错误！'}), 403

# 更新身份信息
@app.route('/updatePersonalInfo', methods=['POST'])
@jwt_required()
def update_personal_info():
    identity = get_jwt_identity()

    user = RegularUser.query.filter_by(id = identity['id']).first()

    json = request.get_json()

    # 如果改名，检查用户名是否重复
    if json['name'] != user.name:
        cuser = RegularUser.query.filter_by(name = json['name']).first()
        if cuser != None:
            return jsonify({'error': '用户名已存在！'}), 400

    user.name = json['name']
    user.birthday = datetime.strptime(json['birthday'], '%Y-%m-%dT%H:%M:%S.%fZ')
    user.gender = json['gender']
    user.phone = json['phone']
    user.district_id = json['district']

    db.session.commit()
    return jsonify({}), 200

# 获取个人身份信息
@app.route('/getPersonalInfo')
@jwt_required()
def get_personal_info():
    identity = get_jwt_identity()
    user = RegularUser.query.filter_by(id = identity['id']).first()

    # 处理城区编号
    district_id = user.district_id
    parts = [district_id[0:i+2] for i in range(0, len(district_id), 2)]
    district_names = []
    
    # 对每组数字进行查询，获取对应的district名称
    for part in parts:
        district = District.query.filter_by(id=part).first()
        if district:
            district_names.append(district.name)
    
    district = "-".join(district_names)

    ret = user.serialize()
    ret['district'] = district

    return jsonify(ret), 200


# 获取气象站身份信息
@app.route('/getStationInfo')
@jwt_required()
def get_station_info():
    identity = get_jwt_identity()
    user = StationUser.query.filter_by(id = identity['id']).first().serialize()
    return jsonify(user), 200


# 更新气象站身份信息
@app.route('/updateStationInfo', methods=['POST'])
@jwt_required()
def update_station_info():
    identity = get_jwt_identity()

    user = StationUser.query.filter_by(id = identity['id']).first()

    json = request.get_json()

    # 如果改名，检查用户名是否重复
    if json['name'] != user.name:
        cuser = StationUser.query.filter_by(name = json['name']).first()
        if cuser != None:
            return jsonify({'error': '气象站名已存在！'}), 400

    user.name = json['name']
    user.longitude = json['longitude']
    user.latitude = json['latitude']

    db.session.commit()
    return jsonify({}), 200


# 获取气象站监测的所有城区
@app.route('/getStationDistricts')
@jwt_required()
def get_station_districts():
    id = get_jwt_identity()['id']
    monitors = Monitor.query.filter_by(user_id=id).all()

    districts = []
    districts_id = []

    for monitor in monitors:
        district_id = monitor.district_id
        parts = [district_id[0:i+2] for i in range(0, len(district_id), 2)]
        district_names = []
        district_id = []
        
        # 对每组数字进行查询，获取对应的district名称
        for part in parts:
            district = District.query.filter_by(id=part).first()
            if district:
                district_names.append(district.name)
            district_id.append(part.ljust(6,'0'))
            
        district_names = "-".join(district_names)
        districts.append({'name': district_names})
        districts_id.append(district_id)

    return jsonify({'districts':districts, 'districts_id': districts_id}), 200


# 更新气象站监测的所有城区
@app.route('/updateStationDistricts', methods=['POST'])
@jwt_required()
def update_station_districts():
    id = get_jwt_identity()['id']
    monitors = Monitor.query.filter_by(user_id=id).all()

    new_districts = request.get_json()['districts']

    for monitor in monitors:
        if monitor.district_id not in new_districts:
            db.session.delete(monitor)
    
    for district in new_districts:
        if district not in [monitor.district_id for monitor in monitors]:
            monitor = Monitor(user_id=id, district_id=district)
            db.session.add(monitor)
            
    db.session.commit()

    return jsonify({}), 200
    


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    