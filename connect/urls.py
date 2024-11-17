from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('upload/', views.upload_assignment, name='upload_assignment'),
    path('admins/', views.get_all_admins, name='get_all_admins'),
]
