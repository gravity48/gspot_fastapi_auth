from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass(frozen=True)
class BaseUser:
    user_id: UUID
    email: str
    phone: str
    avatar: str
    country: str
    created_at: datetime
    updated_at: datetime

    to_dict = asdict


@dataclass(frozen=True)
class AdminUser(BaseUser):
    is_superuser: bool
    user_permissions: List[str] = field(default_factory=list)
    developer_groups: List[str] = field(default_factory=list)
    developer_permissions: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Company:
    created_by: str
    title: str
    description: str
    email: str
    is_confirmed: bool
    created_at: datetime
    is_active: bool
    is_banned: bool

    to_dict = asdict


@dataclass(frozen=True)
class DeveloperUser(BaseUser):
    is_superuser: bool
    company: dict
    groups: List[str] = field(default_factory=list)
    user_permissions: List[str] = field(default_factory=list)

    def __post_init__(self):
        object.__setattr__(self, 'company', Company(**self.company))


@dataclass(frozen=True)
class CustomerUser(BaseUser):
    birthday: datetime


class UserFactory:
    users = {'administrator': AdminUser, 'developer': DeveloperUser, 'customer': CustomerUser}

    def get_user(self, role: str):
        return self.users.get(role)


__all__ = ['CustomerUser', 'AdminUser', 'DeveloperUser', 'UserFactory', 'Company']
