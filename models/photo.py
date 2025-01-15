from create_app import db

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    dynamicpost_id = db.Column(db.Integer, db.ForeignKey('dynamicposts.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "dynamicpost_id": self.dynamicpost_id
        }