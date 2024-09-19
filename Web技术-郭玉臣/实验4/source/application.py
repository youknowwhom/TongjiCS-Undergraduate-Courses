import os
from flask import Flask, render_template, request, flash, url_for, redirect, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from werkzeug.utils import secure_filename
from functools import wraps

db = SQLAlchemy()
app = Flask(__name__, static_url_path='')
app.secret_key = '#iLoveWebDesigning20230501'
# 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# 文件存储路径
app.config['UPLOAD_PIC_FOLDER'] = ".\static\pic"
app.config['UPLOAD_MEDIA_FOLDER'] = ".\static\media"

# 装饰器 要求用户的管理员身份
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = Users.query.filter_by(username = current_user.id).first()
        if not(user.admin):
            return jsonify({'error' : '您需要管理员权限以进行此操作！'}), 403
        return f(*args, **kwargs)
    return decorated


db.init_app(app)
# 数据库中存储的用户信息格式
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

    
# 数据库中存储的媒体信息格式
class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    picSrc = db.Column(db.String, nullable=False)
    mediaSrc = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return '<Media %r>' % self.title
        
    def to_json(self):
        from sqlalchemy.orm import class_mapper
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '登录后方可使用MintPlayer！'
login_manager.login_message_category = "info"

class User(UserMixin):
    pass

# 如果用户名存在则构建一个新的用户类对象，并使用用户名作为ID
# 如果不存在，返回None
@login_manager.user_loader
def load_user(_username):
    user = Users.query.filter_by(username = _username).first()
    if user is not None:
        curU = User()
        curU.id = user.username
        return curU
    
@login_manager.request_loader
def request_loader(request):
    if(request.form.get('username') == None):
        return
    user = Users.query.filter_by(username = request.form['username']).first()
    if user is not None:
        curU = User()
        curU.id = user.username
        return curU
    


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if(request.method == "GET"):
        return render_template("login.html")
    else:
        user = Users.query.filter_by(username = request.form['username']).first()
        if(user and user.password == request.form['password']):
            curr_user = User()
            curr_user.id = request.form['username']

            login_user(curr_user)
            return redirect(url_for('player'))
        else:
            flash('用户名或密码错误！')
            return redirect(url_for('login'))
        

@app.route("/signup", methods=['POST'])
def signup():
    print(request.form)
    if('username' not in request.form or 'password' not in request.form or 'email' not in request.form):
        flash('个人信息填写不全！')
        return redirect(url_for('login'))
    user = Users.query.filter_by(username = request.form['username']).first()
    if user != None:
        flash('该用户名已被占用！')
        return redirect(url_for('login'))
    user = Users(username = request.form['username'], password = request.form['password'], email = request.form['email'], admin=False)
    db.session.add(user)
    db.session.commit()
    # flask log-in进行登录
    curr_user = User()
    curr_user.id = request.form['username']
    login_user(curr_user)
    return redirect(url_for('player'))


@app.route("/player")
@login_required
def player():
    return render_template("player.html", name = current_user.id)


@app.route("/player/getMediaList")
@login_required
def getMediaList():
    medias = Media.query.all()
    mediaList = [media.to_json() for media in medias]
    return jsonify({"mediaList": mediaList})


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    if(request.method == "GET"):
        return render_template("upload.html")
    else:
        files = request.files
        if 'picSrc' not in files or files['picSrc'] == '':
            flash('未上传缩略图！')
            return redirect(request.url)
        elif 'mediaSrc' not in files or files['mediaSrc'] == '':
            flash('未上传媒体源！')
            return redirect(request.url)
        picFileName = secure_filename(files['picSrc'].filename)
        mediaFileName = secure_filename(files['mediaSrc'].filename)
        # 将文件存入到本地
        files['picSrc'].save(os.path.join(app.config['UPLOAD_PIC_FOLDER'], picFileName))
        files['mediaSrc'].save(os.path.join(app.config['UPLOAD_MEDIA_FOLDER'], mediaFileName))
        db.session.add(Media(
                            title = request.form['title'],
                            subtitle = request.form['subtitle'],
                            picSrc =  '/pic/' + picFileName, 
                            mediaSrc = '/media/' + mediaFileName))
        db.session.commit()
        return redirect(url_for('player'))
    

@app.route("/download/<int:media_id>", methods=["GET"])
@login_required
@admin_required
def download(media_id):
    media = Media.query.filter_by(id = media_id).first()
    if(media == None):
        return jsonify({"error" : "该文件不存在！"}), 404
    mediaName = media.mediaSrc.split("/")[-1]   # 取文件名
    try:
        dir = app.config["UPLOAD_MEDIA_FOLDER"]
        return send_from_directory(dir, mediaName, as_attachment=True)
    # 不存在
    except:
        return jsonify({"error" : "该文件不存在！"}), 404


@app.route("/delete/<int:media_id>", methods=["POST"])
@login_required
@admin_required
def delete(media_id):
    media = Media.query.filter_by(id = media_id).first()
    if(media == None):
        return jsonify({"error" : "该文件不存在！"}), 404
    db.session.delete(media)
    db.session.commit()
    return jsonify({}), 200