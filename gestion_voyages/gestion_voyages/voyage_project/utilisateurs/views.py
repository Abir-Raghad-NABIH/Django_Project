# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, ProfileForm, DocumentUploadForm
from .models import VoyageurProfile
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('profile')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'utilisateurs/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'utilisateurs/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    profile, _ = VoyageurProfile.objects.get_or_create(user=request.user)
    return render(request, 'utilisateurs/profile.html', {'profile': profile})

@login_required
def gestion_documents(request):
    profile = request.user.voyageurprofile
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('gestion_documents')
    else:
        form = DocumentUploadForm(instance=profile)
    return render(request, 'utilisateurs/gestion_documents.html', {'form': form, 'profile': profile})
