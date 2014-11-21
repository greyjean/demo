import re
import cStringIO
import string
import StringIO
import random

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from jsonfield import JSONField

from django.db import models
from django.contrib.auth.models import UserManager
from django.core.files import File

class CreatedMixin(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta():
        abstract = True


class User(AbstractBaseUser, CreatedMixin):
    email = models.EmailField(max_length=80, unique=True)
    first_name = models.CharField(u'First name', max_length=40, null=True, blank=True)
    last_name = models.CharField(u'Last name', max_length=40, null=True, blank=True)
    hash = models.CharField(max_length=22, null=True, blank=True)
    company = models.ForeignKey("Company")

    objects = UserManager()
    USERNAME_FIELD = 'email'


    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = ''.join(random.choice(string.ascii_uppercase +\
                string.digits) for _ in range(22))

        super(User, self).save(*args, **kwargs)


class Company(CreatedMixin):
    name = models.CharField(max_length=40)
    json = JSONField(default={})

    @property
    def fingerprints(self):
        try:
            return self.json.get("fingerprints", [])
        except:
            return []

    @property
    def offers(self):
        try:
            return self.json.get("offers", [])
        except:
            return []

    @property
    def campaigns(self):
        try:
            return self.json.get("campaigns", [])
        except:
            return []
