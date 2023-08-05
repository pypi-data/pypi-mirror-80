#!/usr/local/bin/python3.8
# coding=utf-8
"""
Authorizer.
"""
from functools import wraps
import json
from os import environ

from jose import jwt

from lbz.misc import NestedDict, Singleton

from lbz.exceptions import PermissionDenied, ServerError

# NTH: Consider getting that from SSM
CLIENT_SECRET = environ.get("CLIENT_SECRET", "secret")

RESTRICTED = ["*", "self"]
ALL = "*"
ALLOW = 1
DENY = 0
LIMITED_ALLOW = -1


class Authorizer(metaclass=Singleton):
    allow = {}
    deny = {}
    action = None
    outcome = None
    allowed_resource = None
    denied_resource = None

    def __init__(self, resource=None):
        self.resource = resource
        self._permissions = NestedDict()

    def __getitem__(self, y):
        return self._permissions[y]

    def __str__(self):
        return json.dumps({self.resource: self._permissions})

    def __repr__(self):
        return self.__str__()

    def __contains__(self, *args, **kwargs):
        return self._permissions.__contains__(*args, **kwargs)

    def __len__(self):
        return len(self._permissions)

    def __iter__(self):
        return self._permissions.__iter__()

    def add_permission(self, permission_name, function):
        self._permissions[function] = permission_name

    def set_resource(self, resource_name):
        self.resource = resource_name

    def validate(self, function_name):
        if function_name not in self._permissions:
            raise ServerError
        self.action = self._permissions[function_name]
        self.check_deny()
        self.check_allow()
        if self.denied_resource and self.outcome:
            self.outcome = LIMITED_ALLOW
        if self.outcome == DENY:
            raise PermissionDenied

    def set_policy(self, token: str):
        policy = self.decode_authz(token)
        self.allow = policy["allow"]
        self.deny = policy["deny"]
        self.outcome = DENY
        self.allowed_resource = None
        self.denied_resource = None

    def deny_if_all(self, permission):
        if permission == ALL:
            raise PermissionDenied(
                f"You don't have permission to {self.action} on {self.resource}"
            )

    def check_deny(self):
        if self.deny:
            if self.deny_if_all(self.allow.get("*", self.allow.get(self.resource))):
                return
            if d_domain := self.deny.get(self.resource):
                self.deny_if_all(d_domain)
                if resources_to_check := d_domain.get(self.action):
                    self.deny_if_all(resources_to_check)
                    for k, v in resources_to_check.items():
                        self.deny_if_all(k)
                        self.deny_if_all(v)
                    self.denied_resource = resources_to_check

    def allow_if_all(self, permission):
        if permission == ALL:
            self.outcome = ALLOW
            self.allowed_resource = ALL
            return True

    def check_allow(self):
        if not self.allow:
            raise PermissionDenied
        elif self.allow_if_all(self.allow.get("*", self.allow.get(self.resource))):
            return
        elif self.allow:
            if d_domain := self.allow.get(self.resource):
                if self.allow_if_all(d_domain):
                    return
                elif resource_to_check := d_domain.get(self.action):
                    self.outcome = ALLOW
                    self.allowed_resource = resource_to_check.get("allow")
                    self.denied_resource = resource_to_check.get("deny")

    def get_restrictions(self) -> dict:
        return {"allow": self.allowed_resource, "deny": self.denied_resource}

    @staticmethod
    def sign_authz(authz_data: dict) -> str:
        """Generates JWT token"""
        return jwt.encode(authz_data, CLIENT_SECRET, algorithm="HS512")

    @staticmethod
    def decode_authz(token: str) -> dict:
        """Generates dict from JWT token."""
        return jwt.decode(token, CLIENT_SECRET)


def add_authz(permission_name=""):
    def wrapper(func):
        authz = Authorizer()
        authz.add_permission(permission_name or func.__name__, func.__name__)

        @wraps(func)
        def wrapped(self, *func_args, **func_kwargs):
            return func(self, *func_args, **func_kwargs)

        return wrapped

    return wrapper


def authorize(func):
    def wrapped(self, *func_args, **func_kwargs):
        self._authorizer.validate(func.__name__)
        limited_permissions = self._authorizer.get_restrictions()
        return func(self, *func_args, **func_kwargs, restrictions=limited_permissions)

    return wrapped


def set_authz(cls):
    cls._authorizer.set_resource(cls._name or cls.__name__.lower())
    return cls
