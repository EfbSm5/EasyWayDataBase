from create_app import db
from models.user import User
from models.comment import Comment
import json

class DynamicPost(db.Model):
    __tablename__ = 'dynamicposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, default=0)
    date = db.Column(db.String(50), nullable=False)
    like = db.Column(db.Integer, default=0)
    content = db.Column(db.String(500), nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    position = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer,nullable=False)
    comment_id = db.Column(db.Integer,  nullable=True)
    photo=db.Column(db.String(200),nullable=True)



    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "date": self.date,
            "like": self.like,
            "content": self.content,
            "lat": self.lat,
            "lng": self.lng,
            "position": self.position,
            "user_id": self.user_id,
            "comment_id": self.comment_id,
            "photo": json.loads(self.photo) if self.photo else []  
        }

    def set_photos(self, photos):
        self.photo = json.dumps(photos) 
