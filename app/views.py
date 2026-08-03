from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view()
@permission_classes([AllowAny])
def success(_):
    """Health check endpoint.

    Intentionally left open: it is the probe used to verify deploys and
    availability, and it exposes no data.

    Returns:
        A 200 response with a static success payload.
    """
    return Response({'message': 'success'})
