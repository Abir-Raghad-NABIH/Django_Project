from rest_framework import routers
from .views_api import (
    DestinationViewSet, CircuitViewSet, DepartViewSet, OptionViewSet,
    ReservationViewSet, PaiementViewSet
)

router = routers.DefaultRouter()
router.register(r'destinations', DestinationViewSet)
router.register(r'circuits', CircuitViewSet)
router.register(r'departs', DepartViewSet)
router.register(r'options', OptionViewSet)
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'paiements', PaiementViewSet, basename='paiement')
# router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls
