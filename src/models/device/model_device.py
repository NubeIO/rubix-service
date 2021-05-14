from sqlalchemy import UniqueConstraint

from src import db
from src.models.model_base import ModelBase


class DeviceModel(ModelBase):
    __tablename__ = 'devices'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    user_uuid = db.Column(db.String, db.ForeignKey('users.uuid'), nullable=False)
    device_id = db.Column(db.String(80), nullable=True)

    __table_args__ = (
        UniqueConstraint('user_uuid', 'device_id'),
    )

    @classmethod
    def find_by_user_uuid(cls, user_uuid: str):
        return cls.query.filter_by(user_uuid=user_uuid).all()
