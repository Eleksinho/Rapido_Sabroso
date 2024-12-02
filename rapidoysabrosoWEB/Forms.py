from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'user_level']  # Añade los campos que deseas permitir editar


class SelectorForm(forms.ModelForm):
    class Meta:
        model = PageSelector
        fields = ['product_selector', 'price_selector', 'description_selector', 'image_selector', 'logo_selector']
        widgets = {
            'product_selector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: .producto'}),
            'price_selector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: .precio'}),
            'description_selector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: .descripcion'}),
            'image_selector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: .imagen'}),
            'logo_selector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: .logo'}),
        }
