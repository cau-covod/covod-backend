import uuid
import enum
import time
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy_utils import UUIDType, aggregated, URLType
from sqlalchemy_utils.types.password import PasswordType
from sqlalchemy_utils.types.json import JSONType
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2TokenMixin,
)

db = SQLAlchemy()


user_courses = db.Table("user_courses", db.Model.metadata,
                        db.Column("user_id", db.ForeignKey("covod_user.id")),
                        db.Column("course_id", db.ForeignKey("course.id")),
                        )


class MediaType(enum.Enum):
    VIDEO_ONLY = 1
    AUDIO_ONLY = 2
    AUDIO_VIDEO = 3


class Timestamps(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUIDType(binary=False), unique=True, nullable=False)
    json = db.Column(JSONType())
    lecture_id = db.Column(db.Integer, db.ForeignKey("lecture.id", ondelete="CASCADE"))
    lecture = db.relationship("Lecture", back_populates="timestamps", uselist=False)


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUIDType(binary=False), unique=True, nullable=False)
    extension = db.Column(db.String(4), nullable=False)
    type = db.Column(Enum(MediaType), nullable=False)
    length = db.Column(db.Integer, default=1337)
    thumbnail = db.Column(db.String(50))
    lecture_id = db.Column(db.Integer, db.ForeignKey("lecture.id", ondelete="CASCADE"))
    lecture = db.relationship("Lecture", back_populates="media", uselist=False)


class PDF(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUIDType(binary=False), unique=True, nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey("lecture.id", ondelete="CASCADE"))
    lecture = db.relationship("Lecture", back_populates="pdf", uselist=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    timestamp = db.Column(db.Integer)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("covod_user.id"))
    user = db.relationship("User")
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    lecture_id = db.Column(db.Integer, db.ForeignKey("lecture.id", ondelete="CASCADE"))
    replies = db.relationship(
        "Comment", backref=db.backref("parent", remote_side=[id]),
        lazy="dynamic")

    @staticmethod
    def get_n():
        return 6

    def save(self):
        db.session.add(self)
        db.session.commit()
        # Dark magic
        prefix = self.parent.path + "." if self.parent else ""
        self.path = prefix + "{:0{}d}".format(self.id, self.get_n())
        db.session.commit()

    def level(self):
        return len(self.path) // self.get_n() - 1


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    media = db.relationship("Media", uselist=False, back_populates="lecture")
    pdf = db.relationship("PDF", uselist=False, back_populates="lecture")
    timestamps = db.relationship("Timestamps", uselist=False, back_populates="lecture")
    comments = db.relationship("Comment")

    @aggregated("comments", db.Column(db.Integer))
    def comment_count(self):
        return db.func.count("1")

    def __str__(self):
        return str(self.number)

    def add_comment(self, comment):
        self.comments.append(comment)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUIDType(binary=False), unique=True, nullable=False, default=uuid.uuid4())
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("covod_user.id"))
    lectures = db.relationship("Lecture", backref="course")
    users = db.relationship("User", secondary=user_courses, back_populates="courses")

    def __str__(self):
        return self.name

    def get_users(self):
        return self.users

    def add_user(self, user):
        self.users.append(user)


class User(db.Model):
    __tablename__ = "covod_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True)
    full_name = db.Column(db.String(80))
    password = db.Column(PasswordType(schemes=["pbkdf2_sha512"]))
    courses = db.relationship("Course", secondary=user_courses, back_populates="users")

    def __str__(self):
        return self.username

    def check_password(self, password):
        return self.password == password

    def get_user_id(self):
        return self.id

    def get_courses(self):
        return self.courses


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = "oauth2_client"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("covod_user.id", ondelete="CASCADE"))
    user = db.relationship("User")


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = "oauth2_token"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("covod_user.id", ondelete="CASCADE"))
    user = db.relationship("User")

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()
