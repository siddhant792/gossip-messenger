from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """
    Custom User Manager class
    """

    def create_user(self, mobile_number, password, is_staff=False, is_admin=False):
        if not mobile_number:
            raise ValueError('Users must have an mobile number')

        user = self.model(mobile_number=mobile_number)
        
        user.set_password(password)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, mobile_number, password):
        """
        Creates and saves a staff user with the given mobile_number and password.
        """
        return self.create_user(mobile_number, password, True, False)

    def create_superuser(self, mobile_number, password):
        """
        Creates and saves a superuser with the given mobile_number and password.
        """
        return self.create_user(mobile_number, password, True, True)


class User(AbstractBaseUser):
    """
    Custom user class
    """

    mobile_number = models.CharField(
        unique=True, help_text='Mobile Number', max_length=10, 
        validators=[RegexValidator(r'^[6-9]\d{9}$', 'Please enter a valid mobile number')]
    )
    name = models.CharField(max_length=50, help_text="Name of User")
    is_staff = models.BooleanField(default=False, help_text="This user can access admin panel")
    is_admin = models.BooleanField(
        default=False, help_text="This user has all permissions without explicitly assigning them"
    )
    password = models.CharField(max_length=150)
    summary = models.CharField(
        max_length=500, help_text="Summary of the user", blank=True, default="Hi there! I'm using gossip"
    )
    profile_pic = models.CharField(
        max_length=300, help_text="Profile pic url of the user", blank=True, 
        default='https://www.iiitdm.ac.in/Profile/images/Profile/mdm17d002.png'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'

    def get_name(self):
        # The user is identified by their name
        return f"{self.name}"

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
