from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^index$', views.Index.as_view(), name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^customer_login/$', views.login_user, name='customer_login'),
    url(r'^customer_profile/$', views.customer_profile, name='customer_profile'),
    url(r'^create_student_profile/$', views.create_student_profile, name='create_student_profile'),
    url(r'^(?P<organisation>\w{1,50})/class_list/$', views.classList, name='class_list'),
    url(r'^(?P<organisation>\w{1,50})/class_detail/(?P<class_id>\d+)/$', views.class_detail, name='class_detail'),
    url(r'^(?P<organisation>\w{1,50})/student_register/(?P<class_id>\d+)/$', views.create_student_profile, name='class_detail'),
    url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^class_search/',views.search, name='search'),
    url(r'^class_history/',views.class_history, name='class_history'),
]



