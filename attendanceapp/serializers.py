from rest_framework import serializers
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *


User =get_user_model()







class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['username', 'password','first_name','email']
    
    def save(self): 
        username=self.context['username']
        password=self.context['password']
        first_name=self.context['first_name']
        email=self.context['email']
        print(username)
        user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name)
        return user
    

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model=student
        fields= ['roll_no',]
    
    def validate(self,data):
     return data

    def save(self):
        user=self.context['user']
        photo=self.context['photo']
        roll_no=self.context['roll_no']
        std=student.objects.create(user_student=user,photo=photo,roll_no=roll_no)
        return std

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username', 'password']

    #  this funtion workks when you hit .is_valid() function
    def validate(self,data):
        username=data.get('username')
        password=data.get('password') 
       # this funtion returned data appers in validated_data
        if username and password:
            user=authenticate(username=username,password=password)
            if user is None:               
                 raise serializers.ValidationError("Invalid Credentials")
            else:
                data['user']=user
                return data
        else:
              raise serializers.ValidationError("Invalid Credentials")

class ProxyStudentSerializer(serializers.ModelSerializer):


    username=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    first_name=serializers.SerializerMethodField()

    class Meta:
        model=student
        fields= ['roll_no','user_student','username','email','first_name','photo','can_mark_attendance_now','photo_to_be_matched']
    def get_username(self, user_student):
        return user_student.user_student.username
    def get_email(self, user_student):
        return user_student.user_student.email
    def get_first_name(self,user_student):
        return user_student.user_student.first_name
    
        
class Attendance_serializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    first_name=serializers.SerializerMethodField()
    class Meta:
       model=attendance
       fields=['username','email','first_name','subject_attende','present']
    def get_username(self, user_student):
        return user_student.subject_attende.user_student.username
    def get_email(self, user_student):
        return user_student.subject_attende.user_student.email
    def get_first_name(self,user_student):
        return user_student.subject_attende.user_student.first_name
    
class MissingPerson_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Missingperson
        fields='__all__'
    
    
class FoundPerson_Serializer(serializers.ModelSerializer):
    class Meta:
        model= Foundperson
        fields='__all__'
        
class Testing_serializer(serializers.ModelSerializer):
    class Meta:
        model= testingmodel
        fields='__all__'
        