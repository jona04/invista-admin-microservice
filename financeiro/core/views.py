import math
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView, Response
from datetime import date, datetime, timedelta
from collections import Counter

from core.models import Servico, Nota
from .serializers import ServicoSerializer, ServicoFastSerializer, NotaFastSerializer
from .services import UserService

class RegisterApiView(APIView):
    def post(self, request):
        data = request.data
        data['is_financeiro'] = True
        
        response = UserService.post('register', data=data)

        return Response(response)


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
    def get(self, _):
        servicos = Servico.objects.all()
        serializer = ServicoSerializer(servicos, many=True)
        return Response(serializer.data)


class ServicoBackendAPIView(APIView):
    def get(self, request):

        start_date = datetime.now() - timedelta(30)
        servicos = Servico.objects.filter(created_at__range=(start_date.date(), date.today()))
        serializer = ServicoFastSerializer(servicos, many=True).data

        s = request.query_params.get('s', None)
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

        per_page = total
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * per_page
        end = page * per_page

        servico_quantity_chart = []
        servico_value_chart = []
        count_elements = 0
        count_value = 0
        data = serializer[start:end]
        aux_date = datetime.strptime(data[0]['created_at'],'%Y-%m-%dT%H:%M:%S.%fZ').date()
        for i, d in enumerate(data):
            created_at = d['created_at']
            created_at_date = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
            new_date = created_at_date.date()
            if aux_date == new_date:
                count_elements = count_elements + 1
                count_value = count_value + d['valor_total_servico']
            if aux_date != new_date or i == len(data)-1:
                servico_quantity_chart.append(
                    {
                        'x': aux_date,
                        'y': count_elements
                    }
                )
                servico_value_chart.append(
                    {
                        'x': aux_date,
                        'y': count_value
                    }
                )
                count_elements = 1
                count_value = d['valor_total_servico']
                aux_date = new_date
                continue
        
        return Response({
            'data': {
                'servico_quantity_chart': servico_quantity_chart,
                'servico_value_chart': servico_value_chart
            },
            'meta': {
                'total': total,
                'page': page,
                'last_page': math.ceil(total / per_page)
            }
        })


class ServicoFastGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin):
    queryset = Servico.objects.all()[:100]
    serializer_class = ServicoFastSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)

        return self.list(request)


class NotaBackendAPIView(APIView):
    def get(self, request):

        start_date = datetime.now() - timedelta(30)
        servicos = Nota.objects.filter(created_at__range=(start_date.date(), date.today()))
        serializer = NotaFastSerializer(servicos, many=True).data

        total = len(serializer)

        per_page = total
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * per_page
        end = page * per_page

        data = serializer[start:end]
        for d in data:
            created_at = d['created_at']
            created_at_date = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
            new_date = created_at_date.date()
            d['new_date'] = new_date

        nota_quantity_chart = []
        nota_value_chart = []
        count_elements = 0
        count_value = 0
        data = serializer[start:end]
        aux_date = datetime.strptime(data[0]['created_at'],'%Y-%m-%dT%H:%M:%S.%fZ').date()
        for i, d in enumerate(data):
            created_at = d['created_at']
            created_at_date = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
            new_date = created_at_date.date()
            if aux_date == new_date:
                count_elements = count_elements + 1
                count_value = count_value + d['valor_total_nota']
            if aux_date != new_date or i == len(data)-1:
                nota_quantity_chart.append(
                    {
                        'x': aux_date,
                        'y': count_elements
                    }
                )
                nota_value_chart.append(
                    {
                        'x': aux_date,
                        'y': count_value
                    }
                )
                count_elements = 1
                count_value = d['valor_total_nota']
                aux_date = new_date
                continue
        
        return Response({
            'data': {
                'nota_quantity_chart': nota_quantity_chart,
                'nota_value_chart': nota_value_chart
            },
            'meta': {
                'total': total,
                'page': page,
                'last_page': math.ceil(total / per_page)
            }
        })


class NotaFastGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin):
    queryset = Nota.objects.all()[:100]
    serializer_class = NotaFastSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)

        return self.list(request)


class ChapaBackendAPIView(APIView):
    def get(self, request):

        start_date = datetime.now() - timedelta(30)
        servicos = Servico.objects.filter(created_at__range=(start_date.date(), date.today()))
        serializer = ServicoFastSerializer(servicos, many=True).data

        total = len(serializer)

        per_page = total
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * per_page
        end = page * per_page

        chapa_quantity_chart = []
        chapa_value_chart = []
        count_elements = 0
        count_value = 0
        data = serializer[start:end]
        aux_date = datetime.strptime(data[0]['created_at'],'%Y-%m-%dT%H:%M:%S.%fZ').date()
        for i, d in enumerate(data):
            created_at = d['created_at']
            created_at_date = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
            new_date = created_at_date.date()
            if aux_date == new_date:
                count_elements = count_elements + d['quantidade']
                count_value = count_value + d['valor_total_servico']
            if aux_date != new_date or i == len(data)-1:
                chapa_quantity_chart.append(
                    {
                        'x': aux_date,
                        'y': count_elements
                    }
                )
                chapa_value_chart.append(
                    {
                        'x': aux_date,
                        'y': count_value
                    }
                )
                count_elements = 1
                count_value = d['valor_total_servico']
                aux_date = new_date
                continue
        
        return Response({
            'data': {
                'chapa_quantity_chart': chapa_quantity_chart,
                'chapa_value_chart': chapa_value_chart
            },
            'meta': {
                'total': total,
                'page': page,
                'last_page': math.ceil(total / per_page)
            }
        })