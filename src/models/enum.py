import enum


class RoleType(enum.Enum):
    ADMIN = 'Admin'
    THIRD_PARTY = 'ThirdParty'


class StateType(enum.Enum):
    VERIFIED = 'Verified'
    UNVERIFIED = 'Unverified'
