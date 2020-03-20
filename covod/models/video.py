from covod import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    has_video = db.Column(db.Boolean(), nullable=False, default=True)