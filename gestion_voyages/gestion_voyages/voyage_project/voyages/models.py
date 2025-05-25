from django.db import models
from django.urls import reverse
from django.conf import settings

class Destination(models.Model):
    nom = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')

    def __str__(self):
        return self.nom

class Circuit(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='circuits')
    titre = models.CharField(max_length=255)
    description = models.TextField()
    image_principale = models.ImageField(upload_to='circuits/')
    itineraire = models.TextField()
    points_interet = models.TextField()
    duree = models.PositiveIntegerField(help_text="Durée en jours")

    def __str__(self):
        return f"{self.titre} ({self.destination.nom})"

    def get_absolute_url(self):
        return reverse('circuit_detail', kwargs={'circuit_id': self.id})

class Depart(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='departs')
    date_depart = models.DateField()
    disponibilites = models.PositiveIntegerField()

    class Meta:
        ordering = ['date_depart']

    def __str__(self):
        return f"{self.circuit.titre} – {self.date_depart}"

class Option(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='options')
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.nom} ({self.circuit})"


class Reservation(models.Model):
    voyageur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    depart = models.ForeignKey(Depart, on_delete=models.CASCADE, related_name='reservations')
    nombre_voyageurs = models.PositiveIntegerField()
    date_reservation = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
    ], default='en_attente')

    def __str__(self):
        return f"Réservation de {self.voyageur} pour {self.depart}"

class ReservationOption(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='options')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.option.nom} x {self.quantite}"

class Paiement(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, related_name='paiements')
    date_paiement = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode = models.CharField(
        max_length=30,
        choices=[
            ('CB', 'Carte bancaire'),
            ('virement', 'Virement'),
            ('espece', 'Espèces')
        ]
    )
    statut = models.CharField(
        max_length=20,
        choices=[
            ('effectue', 'Effectué'),
            ('en_attente', 'En attente')
        ],
        default='effectue'
    )
    acompte = models.BooleanField(default=False)  # True si c'est un acompte, False sinon

    def __str__(self):
        return f"{self.reservation} - {self.montant} DH - {self.get_mode_display()}"

class Notification(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sujet} ({'lu' if self.lu else 'non lu'})"