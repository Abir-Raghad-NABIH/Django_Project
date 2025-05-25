from django import forms
from .models import Depart, Option

class ReservationForm(forms.Form):
    depart = forms.ModelChoiceField(queryset=Depart.objects.all(), label="Départ")
    nombre_voyageurs = forms.IntegerField(min_value=1, label="Nombre de voyageurs")
    options = forms.ModelMultipleChoiceField(
        queryset=Option.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Options"
    )

    def __init__(self, *args, **kwargs):
        circuit = kwargs.pop('circuit', None)
        super().__init__(*args, **kwargs)
        if circuit:
            self.fields['depart'].queryset = circuit.departs.filter(disponibilites__gt=0)
            self.fields['options'].queryset = circuit.options.all()

    def clean(self):
        cleaned_data = super().clean()
        depart = cleaned_data.get('depart')
        nombre = cleaned_data.get('nombre_voyageurs')
        if depart and nombre:
            if nombre > depart.disponibilites:
                raise forms.ValidationError("Nombre de places insuffisant pour ce départ.")
        return cleaned_data
    

class PaiementForm(forms.Form):
    montant = forms.DecimalField(label="Montant à payer", min_value=0)
    mode = forms.ChoiceField(choices=[
        ('CB', 'Carte bancaire'),
        ('virement', 'Virement'),
        ('espece', 'Espèces')
    ])
