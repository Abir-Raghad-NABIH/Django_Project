from django.shortcuts import render, get_object_or_404, redirect
from .models import Destination, Circuit
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Circuit, Reservation, ReservationOption, Paiement, Notification
from .forms import ReservationForm, PaiementForm
from decimal import Decimal
from rest_framework import viewsets, permissions



@login_required
def catalogue(request):
    circuits = Circuit.objects.all()
    destinations = Destination.objects.all()

    # Filtres
    destination_id = request.GET.get('destination')
    duree_max = request.GET.get('duree')
    mot_cle = request.GET.get('q')

    if destination_id:
        circuits = circuits.filter(destination_id=destination_id)
    if duree_max:
        circuits = circuits.filter(duree__lte=duree_max)
    if mot_cle:
        circuits = circuits.filter(titre__icontains=mot_cle)

    context = {
        'circuits': circuits,
        'destinations': destinations,
        'filtre_destination': destination_id,
        'filtre_duree': duree_max,
        'filtre_mot_cle': mot_cle,
    }
    return render(request, 'voyages/catalogue.html', context)

@login_required
def circuit_detail(request, circuit_id):
    circuit = get_object_or_404(Circuit, pk=circuit_id)
    departs = circuit.departs.all()
    options = circuit.options.all()
    return render(request, 'voyages/circuit_detail.html', {
        'circuit': circuit,
        'departs': departs,
        'options': options
    })


@login_required
def reserver_circuit(request, circuit_id):
    circuit = get_object_or_404(Circuit, pk=circuit_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, circuit=circuit)
        if form.is_valid():
            depart = form.cleaned_data['depart']
            nombre = form.cleaned_data['nombre_voyageurs']
            options = form.cleaned_data['options']

            # Calcul du prix de base (à adapter si tu ajoutes un champ prix au modèle Circuit)
            prix_base = Decimal(0)
            if hasattr(circuit, 'prix'):
                prix_base = circuit.prix * nombre

            # Calcul du prix des options
            prix_options = sum(opt.prix for opt in options) * nombre
            total = prix_base + prix_options

            # Création de la réservation
            reservation = Reservation.objects.create(
                voyageur=request.user,
                depart=depart,
                nombre_voyageurs=nombre,
                total=total
            )
            for opt in options:
                ReservationOption.objects.create(
                    reservation=reservation,
                    option=opt,
                    quantite=nombre
                )
            # Mise à jour des disponibilités
            depart.disponibilites -= nombre
            depart.save()
            return redirect('confirmation_reservation', reservation_id=reservation.id)
    else:
        form = ReservationForm(circuit=circuit)
    return render(request, 'voyages/reserver.html', {'form': form, 'circuit': circuit})

@login_required
def confirmation_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, voyageur=request.user)
    return render(request, 'voyages/confirmation_reservation.html', {'reservation': reservation})


# @login_required
# def historique_reservations(request):
#     reservations = Reservation.objects.filter(voyageur=request.user).order_by('-date_reservation')
#     return render(request, 'voyages/historique.html', {'reservations': reservations})


@login_required
def historique_reservations(request):
    reservations = Reservation.objects.filter(voyageur=request.user).order_by('-date_reservation')
    # Prépare un dictionnaire {reservation_id: montant déjà payé}
    paiements_dict = {}
    for res in reservations:
        paiements_dict[res.id] = sum(p.montant for p in res.paiements.all())
    return render(request, 'voyages/historique.html', {
        'reservations': reservations,
        'paiements_dict': paiements_dict,
    })


@login_required
def paiement_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, voyageur=request.user)
    paiements = reservation.paiements.all()
    deja_paye = sum(p.montant for p in paiements)
    reste = reservation.total - deja_paye

    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            montant = form.cleaned_data['montant']
            mode = form.cleaned_data['mode']
            acompte = (deja_paye == 0)  # Premier paiement = acompte
            if montant > reste:
                form.add_error('montant', "Vous ne pouvez pas payer plus que le montant restant.")
            else:
                Paiement.objects.create(
                    reservation=reservation,
                    montant=montant,
                    mode=mode,
                    acompte=acompte,
                    statut='effectue'
                )
                # Si tout est payé, statut confirmé
                if montant == reste:
                    reservation.statut = 'confirmee'
                    reservation.save()
                return redirect('facture_reservation', reservation_id=reservation.id)
    else:
        form = PaiementForm(initial={'montant': reste})
    return render(request, 'voyages/paiement.html', {
        'reservation': reservation,
        'form': form,
        'deja_paye': deja_paye,
        'reste': reste,
    })

@login_required
def facture_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, voyageur=request.user)
    paiements = reservation.paiements.all()
    return render(request, 'voyages/facture.html', {
        'reservation': reservation,
        'paiements': paiements,
    })

@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, voyageur=request.user)
    if reservation.statut == 'annulee':
        # Déjà annulée, on peut rediriger ou afficher un message
        return redirect('historique_reservations')
    if request.method == 'POST':
        reservation.statut = 'annulee'
        reservation.save()
        # Optionnel : rembourser ou libérer les places
        reservation.depart.disponibilites += reservation.nombre_voyageurs
        reservation.depart.save()
        return redirect('historique_reservations')
    return render(request, 'voyages/annulation.html', {'reservation': reservation})

@login_required
def mes_notifications(request):
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_envoi')
    # Marquer comme lues
    notifications.filter(lu=False).update(lu=True)
    return render(request, 'voyages/notifications.html', {'notifications': notifications})

