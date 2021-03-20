from django.shortcuts import render, redirect
from django.http import  HttpResponse
from Api.models import MyFile

from django.conf import settings
import boto3
import requests
import cv2

from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser


def ObjectDetection(imagePath):
    session = boto3.Session(profile_name="default")
    Service = session.client("rekognition")
    image = open(imagePath, "rb").read()
    imgH, imgW = cv2.imread(imagePath).shape[:2]
    MyImage = cv2.imread(imagePath)
    response = Service.detect_labels(Image = {"Bytes": image})
    for objects in response["Labels"]:
        if objects["Instances"]:
            objectName = objects["Name"]
            for boxs in objects["Instances"]:
                box = boxs["BoundingBox"]
                x = int(imgW * box["Left"])
                y = int(imgH * box["Top"])
                w = int(imgW * box["Width"])
                h = int(imgH * box["Height"])

                MyImage = cv2.rectangle(MyImage, (x,y), (x+w, y+h), (0,255,0), 2)
                MyImage = cv2.putText(MyImage, objectName, (x,y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [0,0,255], 2)

    cv2.imwrite(imagePath, MyImage)

    return "Its Done..."



def Celebrities_Detection(imagePath):
    session = boto3.Session(profile_name="default")
    Service = session.client("rekognition")
    image = open(imagePath, "rb").read()
    imgH, imgW = cv2.imread(imagePath).shape[:2]
    MyImage = cv2.imread(imagePath)
    response = Service.recognize_celebrities(Image = {"Bytes": image})
    for objects in response["CelebrityFaces"]:
        CelName = objects["Name"]
        Face = objects["Face"]
        box = Face["BoundingBox"]
        x = int(imgW * box["Left"])
        y = int(imgH * box["Top"])
        w = int(imgW * box["Width"])
        h = int(imgH * box["Height"])

        MyImage = cv2.rectangle(MyImage, (x,y), (x+w, y+h), (0,255,0), 2)
        MyImage = cv2.putText(MyImage, CelName, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [0,0,255], 2)

    cv2.imwrite(imagePath, MyImage)




class FileSer(ModelSerializer):
    class Meta:
        model = MyFile
        fields = "__all__"


import base64
import io
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
def ConvertBase64FileintoMemoryFile(Base64Data, filename = "Profile"):
    idx = Base64Data[:50].find(',')
    base64file = Base64Data[idx + 1:]
    attributes = Base64Data[:idx]
    content_type = attributes[len('data:'):attributes.find(';')]
    f = io.BytesIO(base64.b64decode(base64file))
    image = InMemoryUploadedFile(f, field_name='picture', name=f"{filename}.png",
                                 content_type=content_type, size=sys.getsizeof(f), charset=None)
    return image







@api_view(["GET", "POST"])
@renderer_classes([JSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def TestAPI(request):
    if request.method == "POST":
        service = request.POST["service"]
        file = request.data["image"]
        file = ConvertBase64FileintoMemoryFile(file)
        Ser = FileSer(data = request.data)
        if Ser.is_valid():
            Ser.save()
            LastFile = MyFile.objects.get(id = Ser.data['id'])
            imagePath = settings.MEDIA_ROOT + "/" + LastFile.image.name
            imageUrl = "http://127.0.0.1:7000" + LastFile.image.url

            if service == "Object Detection":
                ObjectDetection(imagePath)

            if service == "Cel.. Det...":
                Celebrities_Detection(imagePath)

            print(imagePath, imageUrl)
        return Response(data={"Response":"Face Match"}, status = status.HTTP_200_OK)
        return Response(data={"Response":"Face dNE..."}, status = status.HTTP_200_OK)

        return Response(data={"Url":imageUrl}, status = status.HTTP_200_OK)







    
