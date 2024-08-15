from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя', 'autofocus': 'autofocus'}),
                               label='Имя пользователя',
                               required=True)
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                               label='Пароль',
                               required=True)

# class RegistrationForm(forms.Form):
