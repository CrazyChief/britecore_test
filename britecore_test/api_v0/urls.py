from rest_framework.routers import DefaultRouter
from .views import RiskTypeViewSet, RiskViewSet

router = DefaultRouter()


# risks routes
router.register(r'risk-types', RiskTypeViewSet)
router.register(r'risks', RiskViewSet)
