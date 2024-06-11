from django.urls import path
from . import views

app_name = 'crm'
urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('registro', views.registro, name="registro"),
    path('login', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('empresa/<int:empresa_id>/', views.empresa_detail, name='empresa_detail'),
    path('adicionar_empresa/', views.adicionar_empresa, name='adicionar_empresa')
]
