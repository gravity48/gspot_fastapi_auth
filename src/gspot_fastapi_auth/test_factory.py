from datetime import datetime

import factory
from faker import Faker

from .models import AdminUser, BaseUser, CustomerUser, DeveloperUser

fake = Faker(['ru_Ru'])


class BaseUserFactory(factory.Factory):
    class Meta:
        model = BaseUser

    user_id = factory.Faker('uuid4')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    avatar = ''
    country = factory.Faker('country')
    created_at = str(datetime.now())
    updated_at = str(datetime.now())


class AdminUserFactory(BaseUserFactory):
    class Meta:
        model = AdminUser

    is_superuser = True
    user_permissions = []
    developer_groups = []
    developer_permissions = []
    groups = []


class CustomerUserFactory(BaseUserFactory):
    class Meta:
        model = CustomerUser

    birthday = str(datetime.now())


class DeveloperUserFactory(BaseUserFactory):
    class Meta:
        model = DeveloperUser

    is_superuser = True
    company = {
        'created_by': fake.uuid4(),
        'title': fake.word(),
        'description': fake.text(),
        'email': fake.email(),
        'is_confirmed': True,
        'created_at': str(datetime.now()),
        'is_active': True,
        'is_banned': True,
    }
    groups = []
    user_permissions = []


__all__ = ['AdminUserFactory', 'CustomerUserFactory', 'DeveloperUserFactory']
