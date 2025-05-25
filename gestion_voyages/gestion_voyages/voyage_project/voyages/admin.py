from django.contrib import admin
from .models import Destination, Circuit, Depart, Option, Notification
import csv
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages

class DestinationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser  # Seuls superusers peuvent ajouter

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class CircuitAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class DepartAdmin(admin.ModelAdmin):
    list_display = ('circuit', 'date_depart', 'disponibilites')
    list_filter = ('circuit', 'date_depart')
    search_fields = ('circuit__titre',)
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class OptionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
from .models import Reservation, Paiement, ReservationOption

class ReservationOptionInline(admin.TabularInline):
    model = ReservationOption
    extra = 0

class PaiementInline(admin.TabularInline):
    model = Paiement
    extra = 0

def export_reservations_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reservations.csv"'
    writer = csv.writer(response)
    writer.writerow(['Voyageur', 'Circuit', 'Départ', 'Nombre', 'Total', 'Statut', 'Date'])
    for r in queryset:
        writer.writerow([
            r.voyageur.username,
            r.depart.circuit.titre,
            r.depart.date_depart,
            r.nombre_voyageurs,
            r.total,
            r.statut,
            r.date_reservation
        ])
    return response
export_reservations_csv.short_description = "Exporter les réservations sélectionnées en CSV"

# def envoyer_message_clients(modeladmin, request, queryset):
#     # Affiche un formulaire pour saisir le message (option avancée)
#     # Ici, on envoie un message simple à tous les clients sélectionnés
#     sujet = "Information concernant votre réservation"
#     message = "Bonjour,\n\nNous vous contactons concernant votre réservation chez Voyage+.\n\nCordialement,\nL'équipe Voyage+"
#     envoyes = 0
#     for reservation in queryset:
#         email = reservation.voyageur.email
#         if email:
#             send_mail(
#                 sujet,
#                 message,
#                 None,  # from_email (utilise DEFAULT_FROM_EMAIL)
#                 [email],
#                 fail_silently=True,
#             )
#             envoyes += 1
#     messages.success(request, f"{envoyes} e-mails envoyés aux clients sélectionnés.")
# envoyer_message_clients.short_description = "Envoyer un e-mail aux clients sélectionnés"


def notifier_clients(modeladmin, request, queryset):
    sujet = "Information concernant votre réservation"
    message = "Bonjour,\n\nVous avez un nouveau message concernant votre réservation sur Voyage+.\n\nCordialement,\nL'équipe Voyage+"
    envoyes = 0
    for reservation in queryset:
        utilisateur = reservation.voyageur
        Notification.objects.create(
            utilisateur=utilisateur,
            sujet=sujet,
            message=message,
        )
        envoyes += 1
    from django.contrib import messages
    messages.success(request, f"{envoyes} notifications créées pour les clients sélectionnés.")
notifier_clients.short_description = "Notifier les clients sélectionnés (notification interne)"


class ReservationAdmin(admin.ModelAdmin):
    actions = [export_reservations_csv, notifier_clients]
    list_display = ('voyageur', 'voyageur_email', 'depart', 'nombre_voyageurs', 'total', 'statut', 'date_reservation')
    def voyageur_email(self, obj):
        return obj.voyageur.email
    voyageur_email.short_description = "Email"
    list_filter = ('statut', 'depart__circuit', 'depart__date_depart')
    search_fields = ('voyageur__username', 'depart__circuit__titre')
    inlines = [ReservationOptionInline, PaiementInline]
    readonly_fields = ('date_reservation',)


admin.site.register(Destination, DestinationAdmin)
admin.site.register(Circuit, CircuitAdmin)
admin.site.register(Depart, DepartAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Paiement)
admin.site.register(ReservationOption)