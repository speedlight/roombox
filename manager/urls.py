from django.conf.urls import url

from . import views

app_name = 'manager'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
