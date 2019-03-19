from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import RiskTypeViewSet, RiskViewSet

router = DefaultRouter()


# risks routes
router.register(r'risk-types', RiskTypeViewSet)
router.register(r'risk', RiskViewSet)

urlpatterns = [
    url(r'^risk-types/(?P<pk>\d+)/risk/',
        RiskViewSet.as_view({'get': 'list'}))
]

urlpatterns += router.urls
