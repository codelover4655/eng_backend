
from celery import shared_task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import *
from rest_framework import permissions
from rest_framework import generics,mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.files.base import ContentFile
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
ENDPOINT = "https://engage4655.cognitiveservices.azure.com/"
PERSON_GROUP_ID = str(uuid.uuid4())

KEY = "96aa79f0f2be4acca4208632a8e201ee"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)


User =get_user_model()



# command to run celery "celery -A eng_backend worker --pool=solo -l info"







username='missingpeople4655@gmail.com'
password='missingpeople'

                                                #no change needed
def send_mail(html=None,subject='Yeah We Found A Match',from_email='missingpeople4655@gmail.com',to_emails=[],text=''):
    assert isinstance(to_emails,list)
    msg=MIMEMultipart('alternative')
    msg['From']=from_email
    msg['To']=", ".join(to_emails)
    msg['Subject']=subject
    txt_part=MIMEText(text,'plain')
    msg.attach(txt_part)
    html_part = MIMEText(f"<p>Recently someone Found a Person Matching the Profile You filed Missing Complian For</p> <a href='http://localhost:3000/Profile_Found_Verdict/{html}'>Profile</a> </h1>", 'html')
    msg.attach(html_part)
    msg_str=msg.as_string()
    server=smtplib.SMTP(host='smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(from_email,to_emails,msg_str)
    server.quit()



def send_mail1(html=None,subject='Yeah We Found A Match',from_email='missingpeople4655@gmail.com',to_emails=[],text=''):
    assert isinstance(to_emails,list)
    msg=MIMEMultipart('alternative')
    msg['From']=from_email
    msg['To']=", ".join(to_emails)
    msg['Subject']=subject
    txt_part=MIMEText(text,'plain')
    msg.attach(txt_part)
    html_part = MIMEText(f"<p>Recently someone Found a Person Matching the Profile You filed Found  Complian For</p> <a href='http://localhost:3000/Profile_Missing_Verdict/{html}'>Profile</a> </h1>", 'html')
    msg.attach(html_part)
    msg_str=msg.as_string()
    server=smtplib.SMTP(host='smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(from_email,to_emails,msg_str)
    server.quit()


@shared_task(bind=True)
def send_match_mail_missing(self,id):
        print("testing")
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
                if data_from_api.get('isIdentical','False')==True:
                    dict[cnt]+=1
        cnt=1
        for i in data_m:
            if dict[cnt]>=1:
                send_mail(html=i['id'],to_emails=[serl.data['email']]) 
                send_mail1(html=id,to_emails=[i['email']])                                                         # sending mail of details of matching found faces  to the person who filed missing complain 
            cnt+=1




@shared_task(bind=True)
def send_match_mail_found(self,id):
        obj=get_object_or_404(Foundperson,pk=id)
        serl=FoundPerson_Serializer(obj)
        imageurl=serl.data['photo']
        detected_faces = face_client.face.detect_with_url(url=imageurl, detection_model='detection_03')
        fid1= detected_faces[0].face_id
        q1=Missingperson.objects.all()
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
                if data_from_api.get('isIdentical','False')==True:
                    dict[cnt]+=1
        cnt=1
        for i in data_m:
            if dict[cnt]>=1:
                send_mail1(html=i['id'],to_emails=[serl.data['email']])
                send_mail(html=id,to_emails=[i['email']])           # sending mail of details of matching missing faces  to the person who filed Found complain 
            cnt+=1


   