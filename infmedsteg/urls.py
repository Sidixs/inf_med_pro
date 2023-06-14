from django.urls import path
from infmedsteg import views

urlpatterns = [
    path('', views.view_home.home, name='home'),
    path('home', views.view_home.home, name='home'),
    path('tos', views.view_tos.TOS_page, name='tos'),
    path('signup', views.view_registration.sign_up, name='signup'),
    path('files', views.view_files.allFiles, name='allfiles'),
    path('files/<str:Fid>', views.view_files.choosenFile, name='choosenfile'),
    path('myfiles', views.view_encoded.allEncoded, name='myfiles'),
    path('myfiles/<str:Fid>', views.view_encoded.choosenEncoded, name='choosenencoded'),
]
