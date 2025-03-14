from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # @app.errorhandler(RequestEntityTooLarge)
    # def handle_file_too_large(e):
    #     return "File is too large", 413
    
    # 配置 SQLite 数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///easypoints.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 配置文件上传路径
    app.config['UPLOAD_FOLDER'] = './uploads'
    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 限制文件大小 200MB

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from models.comment import Comment
        from models.user import User
        from models.easypoint import EasyPoint
        from models.dynamicpost import DynamicPost
        from models.file import File
        from models.apk import APK

        db.create_all()

        # 注册蓝图
        from route import main as main_blueprint
        app.register_blueprint(main_blueprint)

    return app
