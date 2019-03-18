from django.utils.translation import ugettext_lazy as _

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from risks.models import RiskType, Risk
from .serializers import RiskTypeSerializer, RiskSerializer


DEFAULT_SCHEMA_ITEM_KEYS = [
    'field_name',
    'field_type',
    'options',
    'optionDisabled',
    'is_required',
]


class RiskTypeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """
    API endpoint for listing and creating RiskType objects
    """

    queryset = RiskType.objects.all()
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    serializer_class = RiskTypeSerializer

    def make_check(self, data):
        # Make validation for schema
        correct_schema = True
        flag = None
        if isinstance(data, list) is False:
            correct_schema = False
            flag = 'Schema must be wrapped by Array!'
        else:
            for item in data:
                if isinstance(item, dict):
                    keys = [key for key in item.keys()]
                    if (len(keys) > len(DEFAULT_SCHEMA_ITEM_KEYS)
                            or len(keys) < len(DEFAULT_SCHEMA_ITEM_KEYS)):
                        correct_schema = False
                        flag = 'Incorrect schema item!'
                    else:
                        for k in keys:
                            if k not in DEFAULT_SCHEMA_ITEM_KEYS:
                                correct_schema = False
                                flag = 'Incorrect schema item!'
                                return {
                                    'correct_schema': correct_schema,
                                    'message': flag
                                }
                    return {
                        'correct_schema': correct_schema,
                        'message': flag
                    }
        return {
            'correct_schema': correct_schema,
            'message': flag
        }

    def perform_create(self, serializer):
        errors = self.make_check(self.request.data['schema'])
        if errors['correct_schema'] is False:
            return Response({'Error': errors['message']})
        else:
            serializer.save()

    def perform_update(self, serializer):
        errors = self.make_check(self.request.data['schema'])
        if errors['correct_schema'] is False:
            return Response({'Error': errors['message']})
        else:
            serializer.save()


class RiskViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint for listing, creating, updating and destroying Risk objects
    """

    queryset = Risk.objects.all()
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
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
