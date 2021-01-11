from src import db
from src.platform.model_base import ModelBase


class UsersModel(ModelBase):
    __tablename__ = 'users'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    user_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "Users({})".format(self.uuid)

    @classmethod
    def find_by_user_name(cls, user_uuid):
        return cls.query.filter_by(uuid=user_uuid).first()

