from django.db import models 
from PIL import Image
# from django.contrib import auth
# from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
import os
from django.conf import settings
import string
# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, email, image, username,phno ,password):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')
		if not phno:
			raise ValueError('Users must have a contact number')
		if not password:
			raise ValueError('Password cannot be Empty')
		# path=os.path.join(settings.MEDIA_ROOT,email)
		# os.mkdir(path)
		user = self.model(
			email=self.normalize_email(email),
			username=username,
			phno = phno,
			image=image
			
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_admin(self, email,phno,image , username, password):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')
		if not phno:
			raise ValueError('Users must have a contact number')
		if not password:
			raise ValueError('Password cannot be Empty')
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			phno = phno,
			image=image
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = False
		user.save(using=self._db)
		return user

	def create_superuser(self, email,phno,image , username, password):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')
		if not phno:
			raise ValueError('Users must have a contact number')
		if not password:
			raise ValueError('Password cannot be Empty')
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			phno = phno,
			image=image
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



def user_profile_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.email, filename)

class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=50)
	phno                    = models.CharField(max_length=20)
	image					= models.ImageField(upload_to=user_profile_path,default="default_image.png",null=True,blank=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username','phno']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True