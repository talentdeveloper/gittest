# bot/urls.py
from django.conf.urls import url
from bot import views
# SET THE NAMESPACE!
app_name = 'bot'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^chaturbate_login/$',views.chaturbate_start,name='chaturbate_login'),
    url(r'^chaturbate_logout/$',views.chaturbate_stop,name='chaturbate_logout'),
]