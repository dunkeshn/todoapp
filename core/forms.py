from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя',
                                                             'autofocus': 'autofocus'}),
                               label='Имя пользователя',
                               required=True)
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                               label='Пароль',
                               required=True)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван',
                                                               'autofocus': 'autofocus'}),
                                 label='Имя')

    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}),
                                label='Фамилия',
                                required=False)

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
                             label='Электронная почта')

    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
                               label='Имя пользователя')

    date_of_birth = forms.DateField(label='Дата рождения',
                                    required=False,
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': 'Дата рождения',
                                               'type': 'date'}))

    picture = forms.ImageField(label='Изображение',
                               initial='pictures/default.jpg',
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Изображение',
                                                             'type': 'file'}))

    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Пароль из 8 символов'}),
                               label='Пароль')

    submit_password = forms.CharField(max_length=100,
                                      widget=forms.PasswordInput(
                                          attrs={'class': 'form-control', 'placeholder': 'Пароль из 8 символов'}),
                                      label='Пароль')
