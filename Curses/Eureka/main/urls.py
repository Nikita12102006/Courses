from django.urls import path
from . import views
urlpatterns = [
    path('', views.main_page, name = 'home'),
    path('registration', views.registration, name = 'registration'),
    path('authorization', views.authorization, name = 'authorization')
]