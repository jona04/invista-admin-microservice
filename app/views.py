from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


# Health check. Fica aberto de proposito: e a sonda usada para verificar deploy
# e disponibilidade, e nao expoe nenhum dado.
@api_view()
@permission_classes([AllowAny])
def success(_):
    return Response({'message':'success'})
