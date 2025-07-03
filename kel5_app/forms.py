from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Projek, Meaningful, Experience, Implementasi, Batasan, Relasi,Perencanaan,Profile
from django.forms.widgets import ClearableFileInput

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ProjekForm(forms.ModelForm):
    class Meta:
        model = Projek
        fields = ['nama']



class MeaningfulForm(forms.ModelForm):
    class Meta:
        model = Meaningful
        fields = ['projek', 'objectives', 'outcomes', 'indicator', 'properties', 'tanggal_mulai', 'tanggal_akhir']
        widgets = {
            'projek': forms.HiddenInput()
        }



class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['projek', 'automate', 'prompt', 'annotate', 'organization']
        widgets = {
            'projek': forms.HiddenInput()
        }


class ImplementasiForm(forms.ModelForm):
    class Meta:
        model = Implementasi
        fields = ['projek', 'proses', 'teknologi', 'bangun']
        widgets = {
            'projek': forms.HiddenInput()
        }


class BatasanForm(forms.ModelForm):
    class Meta:
        model = Batasan
        fields = ['projek', 'batasan']
        widgets = {
            'projek': forms.HiddenInput()
        }


class RelasiForm(forms.ModelForm):
    class Meta:
        model = Relasi
        fields = ['projek', 'relasi']
        widgets = {
            'projek': forms.HiddenInput()
        }
class PerencanaanForm(forms.ModelForm):
    class Meta:
        model = Perencanaan
        fields = ['projek','deployment','pemeliharaan','operasi']
        widgets = {
            'projek': forms.HiddenInput()
        }
    



class CustomClearableFileInput(ClearableFileInput):
    template_name = 'custom_widgets/custom_clearable_file_input.html'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto_profil']
        widgets = {
            'foto_profil': CustomClearableFileInput(),
        }