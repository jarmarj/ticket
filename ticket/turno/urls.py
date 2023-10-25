from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("registrar", views.registrar, name="registrar"),
    path('crear/<int:id_muni>', views.crear, name='crear'),
    path('crear/<int:id_muni>/<str:message>', views.crear, name='crear'),
    path('turnos/<int:id_muni>', views.turnos, name='turnos'),
    path('detalles/<int:id_turno>', views.detalles, name='detalles'),
    path('editar/<int:id_turno>', views.editar, name='editar'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:id_muni>', views.dashboard, name='dashboard'),
    path('pronostico/<int:id_muni>', views.pronostico, name='pronostico'),
    path('pdf/<int:turno_id>', views.renderpdf, name='pdf'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
