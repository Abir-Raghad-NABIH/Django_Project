from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'), 
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('documents/', views.gestion_documents, name='gestion_documents'),
]
