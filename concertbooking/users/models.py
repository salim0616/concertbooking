from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models

# Create your models here.


class User(AbstractBaseUser):
    """
    custom user model has been created inheriting AbstractBaseUser.
    we can use choice field to differentiate users but for simplicity using
    boolean mentioning user is artist or not.

    """

    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True)
    is_artist = models.BooleanField(default=False)
    name = models.CharField(max_length=20)

    REQUIRED_FIELDS = ["password", "is_artist", "name"]
    objects = UserManager()

    class Meta:
        db_table = "users"
