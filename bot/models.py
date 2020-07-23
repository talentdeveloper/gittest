from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	#portfolio_site = models.URLField(blank=True)
	profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
	chaturbate_username = models.CharField(max_length=64, blank=True, null=True)
	chaturbate_password = models.CharField(max_length=64, blank=True, null=True)
	def __str__(self):
	  return self.user.username
	  
	  

class CamsLogInfo(models.Model):
	chaturbate_username = models.CharField(max_length=64, blank=True, null=False)
	status = models.CharField(max_length=20, blank=True, null=False,default='Online')