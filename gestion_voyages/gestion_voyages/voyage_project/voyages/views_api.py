from .models import Destination, Circuit, Depart, Option, Reservation, Paiement, Notification
from .serializers import (
    DestinationSerializer, CircuitSerializer, DepartSerializer, OptionSerializer,
    ReservationSerializer, PaiementSerializer
)
from rest_framework import viewsets, permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser

class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAdminUser]
    

class CircuitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer
    permission_classes = [IsAdminUser]

class DepartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Depart.objects.all()
    serializer_class = DepartSerializer
    permission_classes = [IsAdminUser]

class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAdminUser]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Chaque utilisateur ne voit que ses réservations
        return Reservation.objects.filter(voyageur=self.request.user)

class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    permission_classes = [IsAdminUser]



# class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = NotificationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Notification.objects.filter(utilisateur=self.request.user)
