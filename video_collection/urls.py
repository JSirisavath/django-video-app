from django.urls import path

from . import views # The file of all request functions that directs to the HTML pages


urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add_video'),
    path('video_list',views.video_list, name='video_list')
]

