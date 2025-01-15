from create_app import db
from models.user import User


class Comment(db.Model):
    __tablename__ = 'comments'
    index=db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    date = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref='comments')

    def to_dict(self):
        return {
            "index": self.index,
            "comment_id": self.comment_id,
            "user_id": self.user_id,
            "content": self.content,
            "like": self.like,
            "dislike": self.dislike,
            "date": self.date
        }
