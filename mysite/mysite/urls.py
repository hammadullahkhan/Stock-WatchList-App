"""EZtradr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from EZtradrApp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^user/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    url(r'^watch/$', views.WatchList.as_view()),
    url(r'^watch/(?P<pk>[0-9]+)/$', views.WatchDetail.as_view()),
    
    url(r'^asset/$', views.AssetList.as_view()),
    url(r'^asset/(?P<pk>[0-9]+)/$', views.AssetDetail.as_view()),

    #url(r'^pandas/', views.PandasAPI.as_view()),
    url(r'^$', views.index)
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += staticfiles_urlpatterns()
