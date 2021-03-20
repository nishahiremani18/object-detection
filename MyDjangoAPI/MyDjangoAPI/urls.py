
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from MyApi.views import Home, TestAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Home),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)