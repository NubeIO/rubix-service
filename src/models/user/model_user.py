import re

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from src import db
from src.models.enum import RoleType, StateType
from src.models.model_base import ModelBase


class UserModel(ModelBase):
    __tablename__ = 'users'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Enum(RoleType), nullable=False, default=RoleType.THIRD_PARTY)
    state = db.Column(db.Enum(StateType), nullable=False, default=StateType.UNVERIFIED)
    devices = db.relationship('DeviceModel', cascade="all,delete", backref='user', lazy=True)

    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('email'),
    )

    @validates('email')
    def validate_email(self, _, value):
        if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value):
            raise ValueError("Invalid email")
        return value

    @validates('username')
    def validate_username(self, _, value):
        if not re.match("^([A-Za-z0-9_-])+$", value):
            raise ValueError("username should be alphanumeric and can contain '_', '-'")
        return value

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()
