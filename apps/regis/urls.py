from django.conf.urls import url, include
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^submit$', views.submit),
    url(r'^logout$', views.logout),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^user/(?P<id>\d+)$', views.user)
]