from ast import mod
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.contrib.auth import authenticate,get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User =get_user_model()

class student(models.Model):
     user_student=models.ForeignKey(User,on_delete=models.CASCADE)
     roll_no=models.IntegerField(unique=True,blank=False)
     photo=models.ImageField(upload_to='images/', blank=True)
     can_mark_attendance_now=models.BooleanField(default=False)
     faceid1=models.CharField(max_length=150, default='')
     faceid2=models.CharField(max_length=150, default='')
     photo_to_be_matched=models.ImageField(upload_to='images/', blank=True)
class professor(models.Model):
     user_professor=models.ForeignKey(User, on_delete=models.CASCADE)
     secret_key=models.CharField(max_length=150,blank=False,default='')

class  course(models.Model):
     name=models.CharField(max_length=150)
     course_proff=models.ForeignKey(professor,on_delete=models.CASCADE)
     start_time=models.IntegerField(unique=True,blank=False)

class team(models.Model):
     topic=models.ForeignKey(course,on_delete=models.CASCADE)
     course_attende=models.ForeignKey(student,on_delete=models.CASCADE)
     course_proff=models.ForeignKey(professor,on_delete=models.CASCADE)
    
class attendance(models.Model):
     subject_attende=models.ForeignKey(student, on_delete=models.CASCADE)
     present=models.BooleanField(default=False)
     
class testingmodel(models.Model):
  photo1=models.ImageField(upload_to='images/', blank=True)

class Foundperson(models.Model):
     filed_by=models.ForeignKey(User,on_delete=models.CASCADE)
     name=models.CharField(max_length=150)
     photo=models.ImageField(upload_to='images/', blank=True)
     latitude=models.FloatField(default=0.0)
     longitude=models.FloatField(default=0.0)
     father=models.CharField(max_length=150)
     mother=models.CharField(max_length=150)
     age=models.IntegerField(blank=False)
     gender=models.CharField(max_length=150)
     contact_no=PhoneNumberField()
     email=models.EmailField(max_length=254,blank=False)
     address=models.CharField(max_length=150,blank=True)

     
class Missingperson(models.Model):
     filed_by=models.ForeignKey(User,on_delete=models.CASCADE)
     name=models.CharField(max_length=150)
     photo=models.ImageField(upload_to='images/', blank=True)
     latitude=models.FloatField(default=0.0)
     longitude=models.FloatField(default=0.0)
     father=models.CharField(max_length=150)
     mother=models.CharField(max_length=150)
     age=models.IntegerField(blank=False)
     gender=models.CharField(max_length=150)
     contact_no=PhoneNumberField()
     email=models.EmailField(max_length=254,blank=False)
     address=models.CharField(max_length=150,blank=True)

class ageunder20(models.Model):
     foundperson=models.ForeignKey(Foundperson,on_delete=models.CASCADE)

class ageunder40(models.Model):
     foundperson=models.ForeignKey(Foundperson,on_delete=models.CASCADE)

class ageunder60(models.Model):
     foundperson=models.ForeignKey(Foundperson,on_delete=models.CASCADE)

class ageunder80(models.Model):
     foundperson=models.ForeignKey(Foundperson,on_delete=models.CASCADE)

class M_ageunder20(models.Model):
     missingperson=models.ForeignKey(Missingperson,on_delete=models.CASCADE)

class M_ageunder40(models.Model):
     missingperson=models.ForeignKey(Missingperson,on_delete=models.CASCADE)

class M_ageunder60(models.Model):
     missingperson=models.ForeignKey(Missingperson,on_delete=models.CASCADE)

class M_ageunder80(models.Model):
     missingperson=models.ForeignKey(Missingperson,on_delete=models.CASCADE)
     

     
     





