from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/', views.search_query),
    url(r'^hotel_id/(?P<hotel_id>[0-9]+)/$', views.hotel),
    url(r'^index_id/(?P<index_id>[0-9]+)/$', views.hotel_detail),
]