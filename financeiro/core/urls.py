from django.urls import include, path

from .views import (ServicoBackendAPIView, ServicoFrontendAPIView, LoginApiView, 
    LogoutAPIView, RegisterApiView, UserAPIView, ServicoFastGenericAPIView,
    NotaFastGenericAPIView, NotaBackendAPIView)


urlpatterns = [
    path('servicos/fast', ServicoFastGenericAPIView.as_view()),
    path('notas/fast', NotaFastGenericAPIView.as_view()),
    path('servicos/frontend', ServicoFrontendAPIView.as_view()),
    path('servicos/backend', ServicoBackendAPIView.as_view()),
    path('notas/backend', NotaBackendAPIView.as_view()),
    path("register", RegisterApiView.as_view() ),
    path("login", LoginApiView.as_view() ),
    path("user", UserAPIView.as_view()),
    path("logout", LogoutAPIView.as_view())
]
