from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^profile/log/$', views.get_client_id, name='get_client_id'),
    url(r'^class_list$', views.classList, name='class_list'),
    url(r'^create_class/$', views.create_class, name ='create_class'),
    url(r'^student_list/$', views.studentList, name='student_list'),
    # update views
    url(r'^update_class/(?P<pk>[0-9]+)$', views.update_class, name='update_class'),
    url(r'^update_student/(?P<pk>[0-9]+)$', views.Update_Student.as_view(), name='update_student'),
    # list views
    url(r'^user_list$', views.userList, name='user_list'),
    url(r'^create_student/$', views.create_student, name='create_student'),
    url(r'^delete_student/(?P<student_id>[0-9]+)/$', views.delete_student, name='delete_student'),
    url(r'^class_detail/(?P<class_id>[0-9]+)/$', views.class_detail, name='class_detail'),
    url(r'^student_detail/(?P<student_id>[0-9]+)/$', views.student_detail, name='student_detail'),
    url(r'^register$', views.register, name='register'),
    url(r'^staff_login/$', views.login_staff, name='login_staff'),
    url(r'^logout/$', views.logout_staff,  name='logout_staff'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^stripe_setup/',views.stripe_setup, name='setup'),
    url(r'^export/', views.export_students, name='exportexport_students'),
    
]