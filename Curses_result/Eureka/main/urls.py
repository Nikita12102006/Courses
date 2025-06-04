from django.urls import path
from . import views
urlpatterns = [
    path('', views.main_page, name = 'home'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/detail/', views.CourseDetail.as_view(), name='lesson_detail'),
]