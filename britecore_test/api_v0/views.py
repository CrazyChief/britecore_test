from django.utils.translation import ugettext_lazy as _

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from risks.models import RiskType, Risk
from .serializers import RiskTypeSerializer, RiskSerializer


class RiskTypeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API endpoint for listing and creating RiskType objects
    """

    queryset = RiskType.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = RiskTypeSerializer


class RiskViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    API endpoint for listing, creating, updating and destroying Risk objects
    """

    queryset = Risk.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = RiskSerializer

    def perform_create(self, serializer):
        risk = serializer.save()
        message = None

        try:
            risk_type = int(self.request.data['risk_type'])
        except ValueError:
            risk_type = ''
            message = _("Risk Type cannot be empty! "
                        "Please, provide appropriate Risk Type for that Risk.")

        if risk_type:
            risk_type = RiskType.objects.get(id=risk_type)
            risk.risk_type = risk_type
            risk.save()
        else:
            return Response({'Error': message})
