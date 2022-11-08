import math
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.views import APIView, Response
import requests

from core.models import Servico
from .serializers import ServicoSerializer
from .services import UserService

class RegisterApiView(APIView):
    def post(self, request):
        data = request.data
        data['is_financeiro'] = True
        
        response = requests.post('http://172.17.0.1:8001/api/register', data)

        return Response(response.json())


class LoginApiView(APIView):
    def post(self, request):
        data = request.data
        data['scope'] = 'financeiro'


        res = UserService.post('login', data=data)

        response = Response()
        response.set_cookie(key='jwt', value=res['jwt'], httponly=True)
        response.data = {
            'message': 'Success'
        }

        return response


class UserAPIView(APIView):
    def get(self, request):
        return Response(request.user_ms)


class LogoutAPIView(APIView):
    def post(self, request):
        UserService.post('logout', headers=request.headers)

        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'Success'
        }
        return response


class ServicoFrontendAPIView(APIView):
    @method_decorator(cache_page(60*60*2, key_prefix='servicos_frontend'))
    def get(self, _):
        servicos = Servico.objects.all()
        serializer = ServicoSerializer(servicos, many=True)
        return Response(serializer.data)


class ServicoBackendAPIView(APIView):
    def get(self, request):
        serializer = cache.get('servicos_backend')
        if not serializer:
            servicos = list(Servico.objects.all())
            
            serializer = ServicoSerializer(servicos, many=True).data
            cache.set('servicos_backend', serializer, timeout=60*30) #30min
        
        s = request.query_params.get('s', '')
        if s:
            serializer = list([
                p for p in serializer
                if (s.lower() in p['nome']) or 
                    (s.lower() in p['cliente']) or 
                    (s.lower() in p['chapa'])
            ])

        total = len(serializer)

        sort = request.query_params.get('sort', None)
        if sort == 'asc':
            serializer.sort(key=lambda p: p['created_at'])
        elif sort == 'desc':
            serializer.sort(key=lambda p: p['created_at'], reverse=True)

        per_page = 9
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * per_page
        end = page * per_page

        data = serializer[start:end]
        return Response({
            'data': data,
            'meta': {
                'total': total,
                'page': page,
                'last_page': math.ceil(total / per_page)
            }
        })
