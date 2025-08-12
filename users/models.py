from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from cloudinary.models import CloudinaryField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("O usuário precisa ter um e-mail.")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def default_profile():
    return 'avatar/default_avatar.png'

def default_background():
    return 'background/default_background.png'

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    profile_image = CloudinaryField('profile', default='default_avatar_iq42sm', blank=True, null=True)
    background_image = CloudinaryField('background', default='default_background_qnntrv', blank=True, null=True)

    followers = models.ManyToManyField("self", symmetrical=False, related_name='following', blank=True)
    blocked = models.ManyToManyField("self", symmetrical=False, related_name='users_blocked', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
