from create_app import db
from models.user import User

class EasyPoint(db.Model):
    __tablename__ = 'easypoints'

    point_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    info = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(200), nullable=True)  # 存储图片文件名
    refresh_time = db.Column(db.String(50), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer,  nullable=True)

    user = db.relationship('User', backref='easypoints')

    def to_dict(self):
        return {
            "point_id": self.point_id,
            "user_id": self.user_id,
            "name": self.name,
            "type": self.type,
            "info": self.info,
            "location": self.location,
            "photo": self.photo,
            "refresh_time": self.refresh_time,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "lat": self.lat,
            "lng": self.lng,
            "comment_id": self.comment_id
        }

class EasyPointsSimplify:
    def __init__(self, point_id, name, lat, lng):
        self.point_id = point_id
        self.name = name
        self.lat = lat
        self.lng = lng

    def to_dict(self):
        return {
            "point_id": self.point_id,
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng
        }