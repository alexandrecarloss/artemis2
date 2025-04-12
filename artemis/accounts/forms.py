# forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'tipo')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)  # Isso mantém a instância
        user.set_password(self.cleaned_data["password1"])  # Aqui usamos o método do model
        if commit:
            user.save()
            self.save_m2m()  # salva M2M se tiver (opcional, só funciona se o form estiver com um ModelAdmin)
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'tipo', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups')

    def clean_password(self):
        return self.initial["password"]
