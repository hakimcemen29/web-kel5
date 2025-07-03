# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import ProjekAPIViewSet, register_user, terima_proyek_engineering

router = DefaultRouter()
router.register(r'projek', ProjekAPIViewSet, basename='projek-api')

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('projek/', views.projek_view, name='projek'),
    path('projek/delete/<int:id>/', views.delete_projek, name='delete_projek'),
    path('projek/detail/<int:projek_id>/', views.view_projek_detail, name='view_projek_detail'),
    path('meaningful/', views.meaningful_input, name='meaningful'),
    path('experience/', views.experience_input, name='experience'),
    path('implementasi/', views.implementasi_view, name='implementasi'),
    path('batasan/', views.batasan_view, name='batasan'),
    path('status/', views.statusRelasi_view, name='status'),
    path('perencanaan/', views.perencanaan_view, name='perencanaan'),
    path('profil/', views.profil_view, name='profil'),
    path('home/', views.home_view, name='home'),
    # path('tess/', views.view_tess, name='tess'),
    path('projek/chart-data/', views.projek_chart_data, name='projek_chart_data'),
    path('api/terima_proyek/', terima_proyek_engineering, name='terima_proyek'),
    path('api/', include(router.urls)),
    
    path('api/register/', register_user, name='api-register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    
    
    path('integrasi/', views.integrasi_view, name='integrasi'),
    path('creation/', views.kirim_ke_teman, name='creation'),
    
    path('integrasi/delete/<int:id>/', views.delete_integrasi_proyek, name='delete_integrasi_proyek'),
    
    path('kirimmanagement/', views.kirim_management_ke_teman, name='kirim_management_ke_teman'),


    
]
