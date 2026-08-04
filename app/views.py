from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny


@api_view()
@authentication_classes([])
@permission_classes([AllowAny])
def success(_):
    """Health check endpoint.

    Intentionally left open: it is the probe used to verify deploys and
    availability, and it exposes no data.

    Authentication is disabled rather than merely permitted, so that a caller
    carrying a stale cookie still gets a straight answer — the probe must
    report on the service, not on the caller's credentials.

    Returns:
        A 200 response with a static success payload.
    """
    return Response({'message': 'success'})
