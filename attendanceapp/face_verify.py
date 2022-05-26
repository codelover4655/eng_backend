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
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition


# This key will serve all examples in this document.
KEY = "96aa79f0f2be4acca4208632a8e201ee"

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://engage4655.cognitiveservices.azure.com/"


PERSON_GROUP_ID='engage-4655'

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
