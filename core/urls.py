from django.urls import path, include

from . import views
from .views import index
urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('mapa/', views.mostra_ocorrencia, name='mapa'),
    path('cadastrar/', views.cadastrarForm, name='cadastrar'),

]