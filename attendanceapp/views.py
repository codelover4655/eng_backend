import re
import base64
from tkinter import E
import json
from turtle import st
from django.http.response import Http404
from django.http import JsonResponse
from msrest import Serializer
from .task import send_match_mail_found
from .task import  send_match_mail_missing
from rest_framework import permissions
from rest_framework import generics,mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser      # we need form parsser as we are sending a form from frontend 
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import OrderedDict
from django.core.files.base import ContentFile
from .models import *
from django.views.decorators.clickjacking import xframe_options_exempt
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
KEY = "96aa79f0f2be4acca4208632a8e201ee"
ENDPOINT = "https://engage4655.cognitiveservices.azure.com/"
PERSON_GROUP_ID = str(uuid.uuid4())
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

baseurl='http://127.0.0.1:8000'


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'

User =get_user_model()

def create_auth_token(user):
    token1,_= Token.objects.get_or_create(user=user)
    #serializer=TokenSerializer(token1)
    #print(serializer.data)
    return token1.key



class  Student_register(generics.GenericAPIView):

     def post(self, request):
         
         username=request.data['username']
         password=request.data['password']
         first_name=request.data['first_name']
         email=request.data['email']
         pic=request.data['photo']
         print(username)
         print(password)
         print(first_name)
         print(email)
         registerserializer=RegisterSerializer(data=request.data,context={'username':username,'password':password,'first_name':first_name,'email':email})       
         if  registerserializer.is_valid():   
                user=registerserializer.save()
                format, imgstr = pic.split(';base64,')   
                ext = format.split('/')[-1] 
                pic = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)  
                roll_no=request.data['roll_no']           
                student_serializer=StudentSerializer(data=request.data,context={'user':user,'roll_no':roll_no,'photo':pic})  
                student_serializer.is_valid(raise_exception=True)      
                std=  student_serializer.save()
                student_model=ProxyStudentSerializer(std)
                x=student_model.data
                imageurl=x['photo']
                detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
                if not detected_faces:
                    obj1=get_object_or_404(student,id=std.id)
                    obj1.delete()
                    obj2=get_object_or_404(User,id=user.id)
                    obj2.delete()
                    return Response({'happy':'PLEASE CAPTURE YOUR IMAGE CLEARLY'},status=status.HTTP_400_BAD_REQUEST) 
                else:
                    first_image_face_ID = detected_faces[0].face_id
                    std.faceid1=first_image_face_ID
                    std.save()
                    atd=attendance(subject_attende=std,present=False)
                    atd.save()
                    x=create_auth_token(user)
                    return Response({'Token': x,'id':std.id},status=status.HTTP_200_OK)
    
         else:
            
            return Response(registerserializer.errors, status=status.HTTP_401_UNAUTHORIZED)




class professor_register(generics.GenericAPIView):

     def post(self, request):
         username=request.data['username']
         password=request.data['password']
         secret_key=request.data['secretkey']
         loginserializer=LoginSerializer(data=request.data)
         loginserializer.is_valid(raise_exception=True)  
         user=loginserializer.validated_data['user']
         proff=professor.objects.all().filter( user_professor=user)
         if proff.count():
               for obj in proff.iterator():
                   if obj.secret_key !=secret_key:
                       return Response({'happy':'INVALID SECRET KEY'},status=status.HTTP_200_OK) 
                
               x=create_auth_token(user)
               return Response({'Token': x,'id':user.first_name},status=status.HTTP_200_OK)
             
         else: return Response(serializers.ValidationError("Invalid Credentials"),status=status.HTTP_400_BAD_REQUEST)

         




class  StudentList(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request): 
        q1=student.objects.all()  # it is a queryset
        student_serializer=ProxyStudentSerializer(q1,many=True)
        q3=student_serializer.data
        return Response(q3, status=status.HTTP_200_OK)



class StudentAttendanceActivation(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):

        token=request.data['token']
        user = Token.objects.get(key=token).user
        q1=professor.objects.all().filter(user_professor=user)
        if q1.count:
            print("tumshar")
            student_list=student.objects.all()
            for obj in student_list.iterator():
                obj.can_mark_attendance_now=True
                obj.save()
            return Response({'happy':'happy'},status=status.HTTP_200_OK) 
                 
        else:
           return  Response({'data': 'ONLY ADMIN ALLOWED'},status=status.HTTP_200_OK)
             
            


class StudentDashboard(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token=request.data['token']
        user = Token.objects.get(key=token).user
        q1=student.objects.all().filter(user_student=user)
        if q1.count:
            std=1
            for i in q1.iterator():
                std=i
                break
            std_serializer=ProxyStudentSerializer(std)
            return Response(std_serializer.data,status=status.HTTP_200_OK)
        else:
            return  Response({'data': 'INVALID USER'},status=status.HTTP_200_OK)


class VerifyImage(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        token=request.data['token']
        user = Token.objects.get(key=token).user
        q1=student.objects.all().filter(user_student=user)
        if q1.count:
            for i in q1.iterator():
                std=i
                break
            pic=request.data['photo']
            format, imgstr = pic.split(';base64,')   
            ext = format.split('/')[-1] 
            pic = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            std.photo_to_be_matched=pic
            std.save()
            std_serializer=ProxyStudentSerializer(std)
            print(std_serializer.data)
            imageurl=std_serializer.data['photo_to_be_matched']
            detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
            if not detected_faces:
                 return  Response({'happy': 'FACE NOT DETECTED '},status=status.HTTP_400_BAD_REQUEST)
            else:
                 first_image_face_ID = detected_faces[0].face_id
                 std.faceid2=first_image_face_ID
                 imageurl=std_serializer.data['photo']
                 detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
                 fc1=detected_faces[0].face_id
                 std.faceid1=fc1
                 std.save()
                 external_api_url = 'https://engage4655.cognitiveservices.azure.com/face/v1.0/verify'
                 data1={
                   'faceId1': std.faceid1,
                    'faceId2': std.faceid2,
                     }
                 res = requests.post(external_api_url, json=data1, headers={"Ocp-Apim-Subscription-Key":"96aa79f0f2be4acca4208632a8e201ee","Content-Type":"application/json"})
                 print(res.json())
                 data_from_api=res.json()
                 print(data_from_api)
                 if data_from_api['isIdentical']==True:
                      atd1=attendance.objects.all().filter(subject_attende=std)
                      for i in atd1.iterator():
                          atd=i
                          break
                      atd.present=True
                      atd.save()
                      return  Response({'happy':'YEAH WE MARKED YOUR ATTENDANCE'},status=status.HTTP_200_OK)   
                 else: 
                     return  Response({'happy':'PHOTO NOT MATCHED PLEASE TAKE A CLEAR PICTURE'},status=status.HTTP_400_BAD_REQUEST)   
        else: 
             return  Response({'data': 'INVALID USER'},status=status.HTTP_200_OK)



class Attendancesheet(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        q1=attendance.objects.all()
        Atd_serializer=Attendance_serializer(q1,many=True)
        q1=Atd_serializer.data

        return Response(Atd_serializer.data,status=status.HTTP_200_OK)
        
class Missingpersonregister(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request):
        token=request.data['token']
        user = Token.objects.get(key=token).user
        request.data['filed_by']=user.id
        pic=request.data['photo1']
        objj=testingmodel.objects.create(photo1=pic)
        serializer= MissingPerson_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ins=serializer.instance
            serl=Testing_serializer(objj)
            imageurl=serl.data['photo1']
            detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
            if not detected_faces:
                ins.delete()
                return  Response({'happy':'Please Upload a clear picture'},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                first_image_face_ID = detected_faces[0].face_id
                objj.delete()
                send_match_mail_missing.delay(ins.id)
                return  Response({'happy':'YEAH WE MARKED YOUR ATTENDANCE'},status=status.HTTP_200_OK)   


            return  Response({'happy':'YEAH WE MARKED YOUR ATTENDANCE'},status=status.HTTP_200_OK)   
        else:
         print(serializer.errors)
         return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        

class Testing(generics.GenericAPIView):

    def post(self, request):

        id =request.data['id']
        obj=get_object_or_404(Missingperson,pk=id)
        serl=MissingPerson_Serializer(obj)
        imageurl=serl.data['photo']
        detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
        fid1= detected_faces[0].face_id
        q1=Foundperson.objects.all()
        dict={}
        cnt=0
        serializer=FoundPerson_Serializer(q1,many=True)
        data_m=serializer.data
        for itr in data_m:
            cnt+=1
            dict[cnt]=0
            image1url=itr['photo']
            detected_faces = face_client.face.detect_with_url(url=image1url, detection_model='detection_03')
            z=-1
            for y in detected_faces:
                z+=1
                x_id=detected_faces[z].face_id
                external_api_url = 'https://engage4655.cognitiveservices.azure.com/face/v1.0/verify'
                data1={
                   'faceId1': fid1 ,
                    'faceId2': x_id,
                     }
                res = requests.post(external_api_url, json=data1, headers={"Ocp-Apim-Subscription-Key":"96aa79f0f2be4acca4208632a8e201ee","Content-Type":"application/json"})
                data_from_api=res.json()
                
                if data_from_api['isIdentical']==True:
                    dict[cnt]+=1

        ans=[]
        cnt=1
        for i in data_m:
            if dict[cnt]>=1:
                print(i)
            cnt+=1
        return Response(ans,status=status.HTTP_200_OK)

        return Response({'happy':'happy'})
   
        
class Foundpersonregister(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token=request.data['token']
        user = Token.objects.get(key=token).user
        request.data['filed_by']=user.id
        pic=request.data['photo1']
        objj=testingmodel.objects.create(photo1=pic)
        serializer= FoundPerson_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ins=serializer.instance
            serl=Testing_serializer(objj)
            imageurl=serl.data['photo1']
            detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
            if not detected_faces:
                ins.delete()
                return  Response({'happy':'Please Upload a clear picture'},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                first_image_face_ID = detected_faces[0].face_id
                objj.delete()
                send_match_mail_found.delay(ins.id)
                return  Response({'happy':'YEAH WE MARKED YOUR ATTENDANCE'},status=status.HTTP_200_OK)   


            return  Response({'happy':'YEAH WE MARKED YOUR ATTENDANCE'},status=status.HTTP_200_OK)   
        else:
         print(serializer.errors)
         return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class MissingpersonList(generics.GenericAPIView):

    def get(self, request):
        q1=Missingperson.objects.all()
        serializer=MissingPerson_Serializer(q1,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class FoundpersonList(generics.GenericAPIView):
    queryset=Foundperson.objects.all()

    def get(self, request):
        queryset=Foundperson.objects.all()
        print(queryset)
        serializer=FoundPerson_Serializer(queryset,many=True)
        x=serializer.data
        return Response(x,status=status.HTTP_200_OK)


class Missingperson_details(generics.GenericAPIView):

    serializer_class=MissingPerson_Serializer
    def post(self, request):
        id=request.data['userid']
        obj=get_object_or_404(Missingperson,pk=id)
        serializer=MissingPerson_Serializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)

class Foundpersondetails(generics.GenericAPIView):
    serializer_class=FoundPerson_Serializer

    def post(self, request):
        id=request.data['userid']
        obj=get_object_or_404(Foundperson,pk=id)
        serializer=FoundPerson_Serializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)

class Mymissincomplain(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        token =request.data['token']
        user = Token.objects.get(key=token).user
        q1= Missingperson.objects.all().filter(filed_by=user)
        serializer=MissingPerson_Serializer(q1,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class Myfoundcomplain(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        token =request.data['token']
        user = Token.objects.get(key=token).user
        q1= Foundperson.objects.all().filter(filed_by=user)
        serializer=FoundPerson_Serializer(q1,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    
class MatchesFoundface(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        q1=Missingperson.objects.all()
        obj=get_object_or_404(Foundperson,pk=request.data['Foundfaceid'])
        serl=FoundPerson_Serializer(obj)
        imageurl=serl.data['photo']
        detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
        fid1= detected_faces[0].face_id
        dict={}
        cnt=0
        serializer=MissingPerson_Serializer(q1,many=True)
        data_m=serializer.data
        for itr in data_m:
            cnt+=1
            dict[cnt]=0
            image1url=itr['photo']
            detected_faces = face_client.face.detect_with_url(url=image1url, detection_model='detection_03')
            z=-1
            for y in detected_faces:
                z+=1
                x_id=detected_faces[z].face_id
                external_api_url = 'https://engage4655.cognitiveservices.azure.com/face/v1.0/verify'
                data1={
                   'faceId1': fid1 ,
                    'faceId2': x_id,
                     }
                res = requests.post(external_api_url, json=data1, headers={"Ocp-Apim-Subscription-Key":"96aa79f0f2be4acca4208632a8e201ee","Content-Type":"application/json"})
                data_from_api=res.json()
                print(data_from_api)
                
                if data_from_api.get('isIdentical','False')==True:
                    dict[cnt]+=1


        ans=[]
        cnt=1
        for i in data_m:
            if dict[cnt]>=1:
                ans.append(i)
            cnt+=1
        return Response(ans,status=status.HTTP_200_OK)


class MatchesINFoundfaces(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        q1=Foundperson.objects.all()
        obj=get_object_or_404(Missingperson,pk=request.data['Foundfaceid'])
        serl=MissingPerson_Serializer(obj)
        imageurl=serl.data['photo']
        detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
        fid1= detected_faces[0].face_id
        dict={}
        cnt=0
        serializer=FoundPerson_Serializer(q1,many=True)
        data_m=serializer.data
        for itr in data_m:
            cnt+=1
            dict[cnt]=0
            image1url=itr['photo']
            detected_faces = face_client.face.detect_with_url(url=image1url, detection_model='detection_03')
            z=-1
            for y in detected_faces:
                z+=1
                x_id=detected_faces[z].face_id
                external_api_url = 'https://engage4655.cognitiveservices.azure.com/face/v1.0/verify'
                data1={
                   'faceId1': fid1 ,
                    'faceId2': x_id,
                     }
                res = requests.post(external_api_url, json=data1, headers={"Ocp-Apim-Subscription-Key":"96aa79f0f2be4acca4208632a8e201ee","Content-Type":"application/json"})
                data_from_api=res.json()
                print(data_from_api)
                if data_from_api.get('isIdentical','False')==True:
                    dict[cnt]+=1

        ans=[]
        cnt=1
        for i in data_m:
            if dict[cnt]>=1:
                ans.append(i)
            cnt+=1
        return Response(ans,status=status.HTTP_200_OK)


           

class Delete_Missing(generics.GenericAPIView):
     authentication_classes = [BearerAuthentication,]
     permission_classes = (permissions.IsAuthenticated,)

     def post(self, request):
         id=request.data['id']
         obj=get_object_or_404(Missingperson,pk=id)
         obj.delete()
         return Response({'happy':'happy'},status=status.HTTP_200_OK)




class Delete_found(generics.GenericAPIView):
     authentication_classes = [BearerAuthentication,]
     permission_classes = (permissions.IsAuthenticated,)

     def post(self, request):
         id=request.data['id']
         obj=get_object_or_404(Foundperson,pk=id)
         obj.delete()
         return Response({'happy':'happy'},status=status.HTTP_200_OK)














    
