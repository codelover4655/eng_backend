from rest_framework import serializers
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



User =get_user_model()



  


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['username', 'password','first_name','email']

    def create(self, validated_data):        # this funtion returned data appers in serilizer.data
        user=User.objects.create_user(**validated_data)
        print(user)
        return user


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
        print(username)
    
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


 


