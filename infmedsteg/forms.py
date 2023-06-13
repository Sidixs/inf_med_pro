from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe

from infmedsteg.models import ClearFiles


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Nazwa użytkownika", required=True,
                               help_text="Pole wymagane. Do 150 znaków. Tylko litery, cyfry, i znaki @.+-_")
    email = forms.EmailField(label="E-mail", required=True)
    email2 = forms.EmailField(label="Potwierdź E-mail", required=True,
                              help_text='Powtórz ten sam adres E-mail co wcześniej, dla weryfikacji.')
    pass1HelpText = """<ul>
        <li>Hasło nie może być zbyt podobne do pozostałych informacji osobowych.</li>
        <li>Hasło musi mieć conajmniej 8 znaków.</li>
        <li>Hasło nie może znajdować się na liście najpopularniejszych haseł.</li>
        <li>Hasło nie może składać się z samych cyfr.</li>
    </ul>"""
    password1 = forms.CharField(label="Hasło", required=True, widget=forms.PasswordInput,
                                help_text=mark_safe(pass1HelpText))
    #       Your password can’t be too similar to your other personal information.
    #       Your password must contain at least 8 characters.
    #       Your password can’t be a commonly used password.
    #       Your password can’t be entirely numeric.
    password2 = forms.CharField(label="Potwierdź hasło", required=True, widget=forms.PasswordInput,
                                help_text="Powtórz to samo hasło co wcześniej, dla weryfikacji.")
    tos_accepted = forms.BooleanField(label=mark_safe('Akceptuję <a href="/tos">regulamin serwisu</a>'),
                                      required=True)  # nie da się zarejestrować bez akceptacji

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email and email2 and email != email2:
            raise ValidationError("Podane adresy E-mail różnią się od siebie.")

        return email2

    class Meta:
        model = User
        fields = ["username", "email", "email2", "password1", "password2", "tos_accepted"]

class MessageForm(forms.Form):
    title = forms.CharField(label='Tytuł')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':'10'}), label='Wiadomość:')
    class Meta:
        model=forms
        fields=['title','message']