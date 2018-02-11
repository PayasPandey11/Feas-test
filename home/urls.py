from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('tweet', views.tweet, name='tweet'),
    path('search', views.search, name='search'),
    path('follow', views.follow, name='follow'),
]
