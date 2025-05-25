from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.catalogue, name='catalogue'),
#     path('<int:circuit_id>/', views.circuit_detail, name='circuit_detail'),
    
# ]

urlpatterns = [
    path('', views.catalogue, name='catalogue'),
    path('<int:circuit_id>/', views.circuit_detail, name='circuit_detail'),
    path('<int:circuit_id>/reserver/', views.reserver_circuit, name='reserver_circuit'),
    path('reservation/<int:reservation_id>/confirmation/', views.confirmation_reservation, name='confirmation_reservation'),
    path('historique/', views.historique_reservations, name='historique_reservations'),
    path('reservation/<int:reservation_id>/paiement/', views.paiement_reservation, name='paiement_reservation'),
    path('reservation/<int:reservation_id>/facture/', views.facture_reservation, name='facture_reservation'),
    path('reservation/<int:reservation_id>/annulation/', views.annuler_reservation, name='annuler_reservation'),
    path('notifications/', views.mes_notifications, name='mes_notifications'),
]

