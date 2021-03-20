from django.db import models

class MyFile(models.Model):
    image = models.ImageField()





## pip install pillow
## Top Connect this with DataBase we need 2 Com..


#1 . python manage.py makemigrations MyApi
#2. python manage.py migrate