from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from .auth import UserRedisAuth
from .models import AdminUser, CustomerUser, DeveloperUser


def is_customer(user=Depends(UserRedisAuth())):
    if isinstance(user, CustomerUser):
        return user
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Not authenticated')


def is_admin(user=Depends(UserRedisAuth())):
    if isinstance(user, AdminUser):
        return user
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Not authenticated')


def is_developer(user=Depends(UserRedisAuth())):
    if isinstance(user, DeveloperUser):
        return user
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Not authenticated')


__all__ = ['is_developer', 'is_customer', 'is_admin']
