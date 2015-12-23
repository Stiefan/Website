from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.SiteContent, name='SiteContent'),
    url(r'^workshops', views.Workshops, name='workshops'),
]