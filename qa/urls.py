from django.conf.urls import url
from . import views

app_name = 'qa'

urlpatterns = [
    url(r'^$', views.home, name='home'),


    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login'),
    url(r'^logout_user/$', views.logout_user, name='logout'),


    
    url(r'^blog/$',views.blog,name='blog'),
    url(r'^profile/$',views.profile,name='profile'),



    url(r'^(?P<tag_id>[0-9]+)/$', views.questions, name='questions'),


    
    url(r'^answers/(?P<question_id>[0-9]+)/$', views.answers, name='answers'),
    url(r'^userdetails/$', views.userdetails, name='userdetails'),
    url(r'^like/(?P<answer_id>[0-9]+)/$', views.like, name='like'),

    ]


