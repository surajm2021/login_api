from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.utils.timezone import utc


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            print('user must need phone number')
            raise ValueError('Users must have an phone')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_new_user(self, username, name, email, phone, password, user_id):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            print('user must have phone number')
            raise ValueError('Users must have an phone')

        user = self.model(
            phone=phone,
            username=username,
            Name=name,
            email=email,
            user_id=user_id,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, phone, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_ = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )

        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


def has_module_perms(app_label):
    "Does the user have permissions to view the app `app_label`?"
    # Simplest possible answer: Yes, always
    return True


class User(AbstractBaseUser):
    Name = models.CharField(
        verbose_name='name',
        max_length=20,
        null=True,
    )
    email = models.CharField(
        verbose_name='email',
        max_length=20,
        null=True,
    )
    phone = models.CharField(
        verbose_name='phone',
        max_length=20,
        null=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=20,
        unique=True,
    )
    user_id = models.CharField(
        verbose_name='user_id',
        max_length=10,
        null=True,
    )

    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # phone & Password are required by default.

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.username
