from django import forms
from django.contrib.auth.models import User
from .models import VoyageurProfile
from django.contrib.auth.forms import AuthenticationForm

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm = cleaned_data.get("confirm_password")

#         if password != confirm:
#             raise forms.ValidationError("Les mots de passe ne correspondent pas")

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = VoyageurProfile
#         fields = ['preferences', 'documents']

from django import forms
from django.contrib.auth.models import User
from .models import VoyageurProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-800 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600',
            'autocomplete': 'new-password',
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-800 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600',
            'autocomplete': 'new-password',
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-800 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600',
            'autocomplete': 'username',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-gray-800 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600',
            'autocomplete': 'email',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")


class ProfileForm(forms.ModelForm):
    preferences = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-gray-800 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600',
            'rows': 3,
        }),
        required=False
    )
    documents = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full border border-gray-800 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600',
        }),
        required=False
    )

    class Meta:
        model = VoyageurProfile
        fields = ['preferences', 'documents']


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = VoyageurProfile
        fields = ['documents']

