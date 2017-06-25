from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^index$', views.index, name='register'),
    url(r'^register$', views.register, name='register'),
    url(r'^customer_login/$', views.login_user, name='customer_login'),
    url(r'^customer_profile/$', views.customer_profile, name='customer_profile'),
    url(r'^create_student/$', views.create_student, name='create_student'),
    url(r'^checkout/(?P<class_id>\d+)/(?P<student_id>[0-9]+)/$', views.checkout, name='checkout'),
    url(r'^class_list$', views.ClassListView.as_view(), name='class_list'),
    url(r'^class_detail/(?P<class_id>\d+)/$', views.class_detail, name='class_detail'),
    url(r'^logout/$', views.logout_user,  name='logout_user'),
]



