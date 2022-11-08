from django.urls import include, path

from .views import (
    ChapaGenericAPIView, ClienteGenericAPIView, NotaGenericAPIView, ServicoGenericAPIView, 
    ServicoListGenericAPIView, NotaListGenericAPIView, NotaFullGenericAPIView,
    LoginApiView, LogoutAPIView, RegisterApiView, UserAPIView
)


urlpatterns = [
    # path('financeiros', FinanceiroAPIView.as_view()),
    path('chapas', ChapaGenericAPIView.as_view()),
    path('chapas/<str:pk>', ChapaGenericAPIView.as_view()),
    path('clientes', ClienteGenericAPIView.as_view()),
    path('clientes/<str:pk>', ClienteGenericAPIView.as_view()),
    path('servicos', ServicoGenericAPIView.as_view()),
    path('servicos/list', ServicoListGenericAPIView.as_view()),
    path('servicos/<str:pk>', ServicoGenericAPIView.as_view()),
    path('notas', NotaGenericAPIView.as_view()),
    path('notas/list', NotaListGenericAPIView.as_view()),
    path('notas/<str:pk>', NotaGenericAPIView.as_view()),
    path('notas/full/<str:pk>', NotaFullGenericAPIView.as_view()),
    path("register", RegisterApiView.as_view() ),
    path("login", LoginApiView.as_view() ),
    path("user", UserAPIView.as_view()),
    path("logout", LogoutAPIView.as_view())
]
