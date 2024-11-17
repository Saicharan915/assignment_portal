from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_admin, name='register_admin'),
    path('login/', views.login_admin, name='login_admin'),
    path('assignments/', views.view_assignments, name='view_assignments'),
    path('assignments/<str:assignment_id>/accept/', views.update_assignment_status, {'status': 'accepted'}, name='accept_assignment'),
    path('assignments/<str:assignment_id>/reject/', views.update_assignment_status, {'status': 'rejected'}, name='reject_assignment'),
]
