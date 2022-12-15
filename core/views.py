# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins
# from django.core.cache import cache
from rest_framework import exceptions
from collections import defaultdict
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate

from .services import UserService
from .serializers import (ChapaSerializer, ClienteSerializer, NotaListSerializer, 
    NotaSerializer, ServicoListSerializer, ServicoSerializer, NotaFullSerializer, 
    EntradaChapaSerializer, SaidaChapaSerializer, EntradaChapaListSerializer,
    CategoriaEntradaSerializer, CategoriaSaidaSerializer, ChapaEstoqueSerializer,
    ServicoCreateNotaSerializer, SaidaChapaListSerializer)
from core.models import Chapa, Cliente, GrupoNotaServico, Nota, Servico, EntradaChapa, SaidaChapa, CategoriaEntrada, CategoriaSaida


class FinanceiroAPIView(APIView):
    def get(self, request):
        users = request.users_ms
        return Response(filter(lambda a: a['is_financeiro'] == 1, users))


class RegisterApiView(APIView):
    def post(self, request):
        data = request.data
        data['is_financeiro'] = False
        
        response = UserService.post('register', data=data)

        return Response(response)


class LoginApiView(APIView):
    def post(self, request):
        data = request.data
        data['scope'] = 'admin'

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
        response.data = {
            'message': 'Success'
        }
        return response


class ClienteGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Cliente.objects.all().order_by("nome")
    serializer_class = ClienteSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        
        return self.list(request)

    def post(self, request):
        response = self.create(request)
        # producer.produce("financeiro_topic", key="cliente_created", value=json.dumps(response.data))
        return response


    def put(self, request, pk=None):
        response = self.partial_update(request, pk)
        # producer.produce("financeiro_topic", key="cliente_updated", value=json.dumps(response.data))
        return response

    def delete(self, request, pk=None):
        self.destroy(request, pk)
        # producer.produce("financeiro_topic", key="cliente_deleted", value=json.dumps(pk))
        return pk


class ChapaGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Chapa.objects.filter().order_by("nome")
    serializer_class = ChapaSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        
        return self.list(request)

    def post(self, request):
        response = self.create(request)
        # producer.produce("financeiro_topic", key="chapa_created", value=json.dumps(response.data))
        return response

    def put(self, request, pk=None):
        response = self.partial_update(request, pk)
        # producer.produce("financeiro_topic", key="chapa_updated", value=json.dumps(response.data))
        return response

    def delete(self, request, pk=None):
        self.destroy(request, pk)
        # producer.produce("financeiro_topic", key="chapa_deleted", value=json.dumps(pk))
        return pk
    

class ServicoListAPIView(APIView):
    def get(self, request, pk=None):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        servicos = Servico.objects.filter(created_at__range=[start, end]).order_by("-id")
        serializer = ServicoListSerializer(servicos, many=True)

        return Response(serializer.data)


class ServicoCreateNotaListAPIView(APIView):
    def get(self, request, pk=None):
        servicos = Servico.objects.filter().order_by("-id")[:50]
        serializer = ServicoCreateNotaSerializer(servicos, many=True)

        return Response(serializer.data)


class ServicoGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Servico.objects.filter().order_by("-id")
    serializer_class = ServicoSerializer

    # @method_decorator(cache_page(60*60*2, key_prefix='servicos_frontend'))
    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)

        return self.list(request)

    def post(self, request):
        chapa = Chapa.objects.get(pk=request.data['chapa'])
        cliente = Cliente.objects.get(pk=request.data['cliente'])
        request.data['valor_total_servico'] = float(request.data['quantidade']) * chapa.valor
        
        response = self.create(request, chapa=chapa, cliente=cliente)
        
        self.reduce_chapa_estoque(chapa, float(request.data['quantidade']))

        # producer.produce("financeiro_topic", key="servico_created", value=json.dumps(response.data))
        
        # for key in cache.keys('*'):
        #     if 'servicos_frontend' in key or 'servicos_list_admin' in key:
        #         cache.delete(key)
        # cache.delete('servicos_backend')
        return response


    def put(self, request, pk=None):

        # quando servico for atualizado, edita valor total do servico
        self.update_total_service_after_put_servico(request)

        # quando servico for atualizado, edita valor total da nota
        self.update_total_nota_after_put_servico(request, pk)

        self.update_estoque_nota_after_put_servico(request, pk)
        
        response = self.partial_update(request, pk)
        # producer.produce("financeiro_topic", key="servico_updated", value=json.dumps(response.data))

        # for key in cache.keys('*'):
        #     if 'servicos_frontend' in key or 'servicos_list_admin' in key:
        #         cache.delete(key)
        # cache.delete('servicos_backend')

        return response

    def delete(self, request, pk=None):
        servico = Servico.objects.get(pk=pk)
        response = self.destroy(request, pk)

        chapa = Chapa.objects.get(pk=servico.chapa.id)
        self.revert_chapa_estoque(chapa, servico.quantidade)

        # producer.produce("financeiro_topic", key="servico_deleted", value=json.dumps(pk))
        
        # for key in cache.keys('*'):
        #     if 'servicos_frontend' in key or 'servicos_list_admin' in key:
        #         cache.delete(key)
        # cache.delete('servicos_backend')
        return response

    def update_estoque_nota_after_put_servico(self, request, servico_id):
        servico = Servico.objects.get(pk=servico_id)
        chapa = Chapa.objects.get(pk=request.data['chapa'])
        chapa.estoque = chapa.estoque + servico.quantidade
        chapa.estoque = chapa.estoque - float(request.data['quantidade'])
        chapa.save(update_fields=['estoque'])

    def update_total_service_after_put_servico(self, request):
        chapa = Chapa.objects.get(pk=request.data['chapa'])
        request.data['valor_total_servico'] = float(request.data['quantidade']) * chapa.valor

    def update_total_nota_after_put_servico(self, request, servico_id):
        nota_servico_by_servico = GrupoNotaServico.objects.filter(servico_id=servico_id)
        if nota_servico_by_servico.exists():
            nota_servico_by_servico = GrupoNotaServico.objects.get(servico_id=servico_id)
            nota = Nota.objects.get(pk=nota_servico_by_servico.nota.id)
            nota_servico_list_by_nota = GrupoNotaServico.objects.filter(nota_id=nota.id)
            valor_total = 0.0
            for nota_servico_by_nota in nota_servico_list_by_nota:
                if int(nota_servico_by_nota.servico.id) == int(servico_id):
                    chapa = Chapa.objects.get(pk=request.data['chapa'])
                    valor_total = valor_total + (float(request.data['quantidade']) * chapa.valor)
                else:
                    servico_obj = Servico.objects.get(pk=nota_servico_by_nota.servico.id)
                    valor_total = valor_total + servico_obj.valor_total_servico
                    
            nota.valor_total_nota = valor_total
            nota.save()

    def reduce_chapa_estoque(self, chapa, quantidade):
        chapa.estoque = chapa.estoque - quantidade
        chapa.save(update_fields=['estoque'])
    
    def revert_chapa_estoque(self, chapa, quantidade):
        chapa.estoque = chapa.estoque + quantidade
        chapa.save(update_fields=['estoque'])


class NotaListAPIView(APIView):
    def get(self, request):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        notas = Nota.objects.filter(created_at__range=[start, end]).order_by("-id")
        serializer = NotaListSerializer(notas, many=True)

        return Response(serializer.data)


class NotaRelatorioAPIView(APIView):
    def get(self, request):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        notas = Nota.objects.filter(created_at__range=[start, end]).values('servico__chapa__nome', date=TruncDate('created_at')).annotate(quantidade_sum=Sum('servico__quantidade'),created_at_count=Count('date'))
        serializer = self.serialize_nota_relatorio(notas)

        formated = {}
        columns = set()
        for item in serializer:
            columns.add(item['date'].strftime("%m/%d"))
            if item['servico_chapa_nome'] not in formated:
                formated[item['servico_chapa_nome']] = {
                    item['date'].strftime("%m/%d"): item['quantidade_sum']
                }
            else:
                formated[item['servico_chapa_nome']].update({
                    item['date'].strftime("%m/%d"): item['quantidade_sum']
                })

        formated_list = sorted(formated.items())
        for item in formated_list:
            item[1]['total'] = sum(item[1].values())
        
        data = {'columns':sorted(columns), 'data':formated_list}

        return Response(data)

    def serialize_nota_relatorio(self, data):
        result = []
        for item in data:
            result.append({
                'servico_chapa_nome': item['servico__chapa__nome'],
                'date': item['date'],
                'quantidade_sum': item['quantidade_sum'],
                'created_at_count': item['created_at_count']
            })
        return result


class NotaFullGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin):
    queryset = Nota.objects.all()
    serializer_class = NotaFullSerializer

    def get(self, request, pk=None):
        return self.retrieve(request, pk)


class NotaGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

    # @method_decorator(cache_page(60*60*2, key_prefix='notas_frontend'))
    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        
        return self.list(request)

    def post(self, request):
        servico_id_list = request.data['servico']
        servicos_list = []
        valor_total = 0.0
        for servico_id in servico_id_list:
            servico_check = GrupoNotaServico.objects.filter(servico_id=servico_id).first()
            if servico_check == None:
                servico = Servico.objects.get(pk=servico_id)
                valor_total = valor_total + servico.valor_total_servico
                servicos_list.append(servico)
            else:
                raise exceptions.APIException(f'Servico ja esta cadastrado na nota de numero: {servico_check.nota.id}')

        request.data['valor_total_nota'] = valor_total
        nota = self.create(request)
        # producer.produce("financeiro_topic", key="nota_created", value=json.dumps(nota.data))
        
        nota_instance = Nota.objects.get(pk=nota.data['id'])
        for servico in servicos_list:
            grupo_nota_servico = GrupoNotaServico.objects.create(nota=nota_instance, servico=servico)
            # producer.produce("financeiro_topic", key="grupo_nota_servico_created", value=json.dumps(GrupoNotaServicoSerializer(grupo_nota_servico).data))

        nota = Nota.objects.get(pk=nota.data['id'])
        
        # for key in cache.keys('*'):
        #     if 'notas_frontend' in key:
        #         cache.delete(key)
        
        return Response(NotaSerializer(nota).data)

    def put(self, request, pk=None):
        nota_instance = Nota.objects.filter(pk=pk).values_list('servico', flat=True)
        servico_id_list = request.data.pop('servico')
        servico_deleted_from_nota = set(list(nota_instance)) - set(servico_id_list)

        servicos_list = []
        valor_total = 0.0
        for servico_id in servico_id_list:
            nota_check = GrupoNotaServico.objects.filter(servico_id=servico_id).first()
            if nota_check == None:
                servico_obj = Servico.objects.get(pk=servico_id)
                valor_total = valor_total + servico_obj.valor_total_servico
                servicos_list.append(servico_obj)
            elif int(nota_check.nota.id) == int(pk):
                servico_obj = Servico.objects.get(pk=servico_id)
                valor_total = valor_total + servico_obj.valor_total_servico
            else:
                raise exceptions.APIException(f'Servico ja esta cadastrado na nota de numero: {nota_check.nota.id}')

        request.data['valor_total_nota'] = valor_total

        for servico in servicos_list:
            grupo_nota_servico = GrupoNotaServico.objects.create(nota_id=pk, servico=servico)
            # producer.produce("financeiro_topic", key="grupo_nota_servico_created", value=json.dumps(GrupoNotaServicoSerializer(grupo_nota_servico).data))

        # for key in cache.keys('*'):
        #     if 'notas_frontend' in key:
        #         cache.delete(key)
        
        response = self.partial_update(request, pk)
        # producer.produce("financeiro_topic", key="nota_updated", value=json.dumps(response.data))
        
        # delete servico in database removed from the nota
        for servico_deleted in servico_deleted_from_nota:
            GrupoNotaServico.objects.filter(servico=servico_deleted).delete()

        return response

    def delete(self, request, pk=None):
        # for key in cache.keys('*'):
        #     if 'notas_frontend' in key:
        #         cache.delete(key)
        
        self.destroy(request, pk)
        # producer.produce("financeiro_topic", key="nota_deleted", value=json.dumps(pk))
        return pk


class EntradaChapaListAPIView(APIView):
    def get(self, request):
        queryset = EntradaChapa.objects.all().order_by("-id")
        serializer_class = EntradaChapaListSerializer(queryset, many=True)
        return Response(serializer_class.data)


class EntradaChapaGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = EntradaChapa.objects.all().order_by("-created_at")
    serializer_class = EntradaChapaSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        
        return self.list(request)

    def post(self, request):
        # request.data['categoria'] = {'id': request.data['categoria'], 'descricao': 'test'}
        print(request.data)
        response = self.create(request)
        self.adiciona_entrada_no_estoque(request.data)
        # producer.produce("financeiro_topic", key="chapa_created", value=json.dumps(response.data))
        return response

    def put(self, request, pk=None):
        response = self.partial_update(request, pk)
        # producer.produce("financeiro_topic", key="chapa_updated", value=json.dumps(response.data))
        return response

    def delete(self, request, pk=None):
        responde = self.destroy(request, pk)
        self.remove_entrada_do_estoque(pk)
        # producer.produce("financeiro_topic", key="chapa_deleted", value=json.dumps(pk))
        return responde

    def adiciona_entrada_no_estoque(self, data):
        chapa = Chapa.objects.get(pk=data['chapa'])
        if chapa.estoque is None:
            chapa.estoque = 0
        chapa.estoque = chapa.estoque + data['quantidade']
        chapa.save()

    def remove_entrada_do_estoque(self, pk):
        entrada_chapa = EntradaChapa.objects.get(pk=pk) 
        chapa = Chapa.objects.get(pk=entrada_chapa.chapa.id)
        chapa.estoque = chapa.estoque - entrada_chapa.quantidade
        chapa.save()


class SaidaChapaListAPIView(APIView):
    def get(self, request):
        queryset = SaidaChapa.objects.all().order_by("-id")
        serializer_class = SaidaChapaListSerializer(queryset, many=True)
        return Response(serializer_class.data)


class SaidaChapaGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = SaidaChapa.objects.all().order_by("-created_at")
    serializer_class = SaidaChapaSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        
        return self.list(request)

    def post(self, request):
        response = self.create(request)
        self.adiciona_saida_no_estoque(request.data)
        # producer.produce("financeiro_topic", key="chapa_created", value=json.dumps(response.data))
        return response

    def put(self, request, pk=None):
        response = self.partial_update(request, pk)
        # producer.produce("financeiro_topic", key="chapa_updated", value=json.dumps(response.data))
        return response

    def delete(self, request, pk=None):
        response = self.destroy(request, pk)
        self.remove_saida_do_estoque(pk)
        # producer.produce("financeiro_topic", key="chapa_deleted", value=json.dumps(pk))
        return response

    def adiciona_saida_no_estoque(self, data):
        chapa = Chapa.objects.get(pk=data['chapa'])
        chapa.estoque = chapa.estoque - data['quantidade']
        chapa.save()

    def remove_saida_do_estoque(self, pk):
        saida_chapa = SaidaChapa.objects.get(pk=pk) 
        chapa = Chapa.objects.get(pk=saida_chapa.chapa.id)
        chapa.estoque = chapa.estoque + saida_chapa.quantidade
        chapa.save()


class CategoriaEntradaGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = CategoriaEntrada.objects.all()
    serializer_class = CategoriaEntradaSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        
        return self.list(request)

    def post(self, request):
        response = self.create(request)
        return response

    def put(self, request, pk=None):
        response = self.partial_update(request, pk)
        return response

    def delete(self, request, pk=None):
        self.destroy(request, pk)
        return pk


class CategoriaSaidaGenericAPIView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = CategoriaSaida.objects.all()
    serializer_class = CategoriaSaidaSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        
        return self.list(request)

    def post(self, request):
        response = self.create(request)
        return response

    def put(self, request, pk=None):
        response = self.partial_update(request, pk)
        return response

    def delete(self, request, pk=None):
        self.destroy(request, pk)
        return pk


class EstoqueAPIView(APIView):
    def map_reduce(self, iterable, keyfunc, valuefunc=None, reducefunc=None):
        valuefunc = (lambda x: x) if (valuefunc is None) else valuefunc

        ret = defaultdict(list)
        for item in iterable:
            key = keyfunc(item)
            value = valuefunc(item)
            ret[key].append(value)

        if reducefunc is not None:
            for key, value_list in ret.items():
                ret[key] = reducefunc(value_list)

        ret.default_factory = None
        return ret

    def get(self, request):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        chapas = Chapa.objects.filter(estoque__isnull=False)
        entradas = EntradaChapa.objects.filter(data__range=[start, end])
        saidas = SaidaChapa.objects.filter(data__range=[start, end])

        serializer_entradas = EntradaChapaSerializer(entradas, many=True)
        serializer_saidas = SaidaChapaSerializer(saidas, many=True)
        serializer_chapas = ChapaEstoqueSerializer(chapas, many=True)
        
        kfunc_ent = lambda d: d['chapa']
        vfunc_ent = lambda d: int(d['quantidade'])
        rfunc_ent = lambda lst_: sum(lst_) 
        entradas_map = self.map_reduce(serializer_entradas.data, keyfunc=kfunc_ent, valuefunc=vfunc_ent, reducefunc=rfunc_ent)
        
        kfunc = lambda d: d['chapa']
        vfunc = lambda d: int(d['quantidade'])
        rfunc = lambda lst_: sum(lst_) 
        saidas_map = self.map_reduce(serializer_saidas.data, keyfunc=kfunc, valuefunc=vfunc, reducefunc=rfunc)
        
        for item in serializer_chapas.data:
            if item['id'] in saidas_map.keys():
                qtd = saidas_map.pop(item['id'])
                item['saidas'] = qtd
            else:
                item['saidas'] = 0
            
            if item['id'] in entradas_map.keys():
                qtd = entradas_map.pop(item['id'])
                item['entradas'] = qtd
            else:
                item['entradas'] = 0
        
        return Response(serializer_chapas.data)
  