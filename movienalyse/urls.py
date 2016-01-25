"""movienalyse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "movies.views.show_home", name='home'),
    url(r'^list/$', "movies.views.show_list", name='list'),
    url(r'^movie/(?P<id>\d+)/$', "movies.views.show_detail", name='detail'),
    url(r'^movie/(?P<id>\d+)/review/$', "movies.views.new_review", name='review'),
    url(r'^movie/(?P<id>\d+)/newtopic/$', "movies.views.new_topic", name='topic'),
    url(r'^movie/(?P<id1>\d+)/forum/(?P<id2>\d+)/newforum/$', "movies.views.new_comment", name='comment'),
    url(r'^movie/(?P<id1>\d+)/forum/(?P<id2>\d+)/reply/(?P<id3>\d+)/$', "movies.views.new_comment", name='reply'),
    url(r'^movie/(?P<id1>\d+)/forum/(?P<id2>\d+)/$', "movies.views.show_comments", name='comments'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^search/', include('haystack.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
