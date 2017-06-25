from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^class_list$', views.ClassListView.as_view(), name='class_list'),
    url(r'^create_class/$', views.create_class, name ='create_class'),
    url(r'^student_list$', views.StudentListView.as_view(), name='student_list'),
    url(r'^classroom_list$',views.ClassRoomListView.as_view(), name='classroom_list'),
    url(r'^classroom_classlist/(?P<classroom_id>[0-9]+)/$',views.classroom_classlist, name='classroom_list'),
    url(r'^create_classroom/$', views.create_classroom, name='create_classroom'),
    url(r'^user_list$', views.UserListView.as_view(), name='user_list'),
    url(r'^create_student/$', views.create_student, name='create_student'),
    url(r'^delete_student/(?P<student_id>[0-9]+)/$', views.delete_student, name='delete_student'),
    url(r'^class_detail/(?P<class_id>[0-9]+)/$', views.class_detail, name='class_detail'),
    url(r'^classroom_detail/(?P<classroom_id>[0-9]+)/$', views.classroom_detail, name='classroom_detail'),
    url(r'^student_detail/(?P<student_id>[0-9]+)/$', views.student_detail, name='student_detail'),
    url(r'^register$', views.register, name='register'),
    url(r'^staff_login/$', views.login_staff, name='login_staff'),
    url(r'^logout/$', views.logout_staff,  name='logout_staff'),
    url(r'^profile/$', views.profile, name='profile'),
]



