from create_app import db

class APK(db.Model):
    __tablename__ = 'apks'

    version_code = db.Column(db.Integer, nullable=False, primary_key=True)
    version_name = db.Column(db.String(50), nullable=False)
    apk_url = db.Column(db.String(200), nullable=False)
    update_message = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            "version_code": self.version_code,
            "version_name": self.version_name,
            "apk_url": self.apk_url,
            "update_message": self.update_message
        }
