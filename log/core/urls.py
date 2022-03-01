from django.urls import path
from . import views 
urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.loginn,name='login'),
    path('logout',views.logoutt,name='logout'),
    path('reg',views.reg,name='reg'),
    path('test',views.test,name='test'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]