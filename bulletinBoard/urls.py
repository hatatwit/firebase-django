"""bulletinBoard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.homepage, name="home"),

        # Authentication urls
        path('signIn/', views.signIn, name="signin"),
        path('signUp/', views.signUp, name="signup"),
        path('signOut/', views.signOut, name="signout"),
        path('reset/', views.reset, name="reset"),
        path('postReset/', views.postReset),
        path('postsignIn/', views.postsignIn),
        path('postsignUp/', views.postsignUp),

        # Document urls
        path('doc/', views.document, name="doc"),
        path('upload/', views.upload, name="upload"),
        path('postUpload/', views.postUpload),
        path('delete/', views.delete, name="delete"),

        # Post urls
        path('post/', views.post, name="post"),
        path('add/', views.add, name="add"),
        path('postAdd/', views.postAdd),
        path('remove/', views.remove, name="remove"),

        # Event urls
        path('event/', views.agenda, name="event"),
        path('create/', views.create, name="create"),
        path('postCreate/', views.postCreate),
        path('cancel/', views.cancel, name="cancel"),

        path('test/', views.test, name="test")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)