from django import forms
from cities_light.models import Country, Region
from cabinet.models import User, Address
from django.contrib.auth import authenticate

class RegisterPhysicalForm(forms.Form):

    first_name = forms.CharField(max_length=50, label='ПІБ')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=13, label='Телефон')

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False
    )
    city = forms.CharField(max_length=100, required=False)
    street = forms.CharField(max_length=255, required=False)

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    # 👇 ПЕРЕИМЕНОВАЛИ
    avatar = forms.ImageField(required=False)
    is_fop = forms.BooleanField(required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email вже зареєстрований')
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError('Паролі не співпадають')
        return cleaned

    def save(self):
        data = self.cleaned_data

        address = Address.objects.create(
            address_type=Address.TYPE_PHYSICAL,
            country=data.get('country'),
            region=data.get('region'),
            city=data.get('city', ''),
            street=data.get('street', ''),
        )

        user = User.objects.create_user(
            email=data['email'],
            password=data['password1'],
            first_name=data.get('first_name', ''),
            phone=data.get('phone', ''),
            is_fop=data.get('is_fop', False),
            address=address,
            avatar=data.get('avatar'),
        )

        return user


class RegisterLegalForm(forms.Form):

    first_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=13)

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False
    )
    city = forms.CharField(max_length=100, required=False)
    street = forms.CharField(max_length=255, required=False)

    legal_type = forms.ChoiceField(
        choices=[('legal', 'Юр. особа'), ('fop', 'ФОП')]
    )

    company_name = forms.CharField(max_length=200, required=False)
    okpo = forms.CharField(max_length=10, required=False)
    edrpou = forms.CharField(max_length=10, required=False)

    legal_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False
    )
    legal_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False
    )
    legal_city = forms.CharField(max_length=100, required=False)
    legal_street = forms.CharField(max_length=255, required=False)
    legal_zip = forms.CharField(max_length=10, required=False)

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

     
    avatar = forms.ImageField(required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email вже зареєстрований')
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError('Паролі не співпадають')
        return cleaned

    def save(self):
        data = self.cleaned_data
        is_fop = data.get('legal_type') == 'fop'

        address = Address.objects.create(
            address_type=Address.TYPE_LEGAL,
            country=data.get('country'),
            region=data.get('region'),
            city=data.get('city', ''),
            street=data.get('street', ''),
            company_name=data.get('company_name', ''),
            edrpou=data.get('edrpou') if is_fop else '',
            zip_code=data.get('legal_zip', ''),
        )

        user = User.objects.create_user(
            email=data['email'],
            password=data['password1'],
            first_name=data.get('first_name', ''),
            phone=data.get('phone', ''),
            is_fop=is_fop,
            address=address,
            avatar=data.get('avatar'),
        )

        return user

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email*'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль*'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(email=email, password=password)
            if not self.user:
                raise forms.ValidationError('Невірний email або пароль')
            if not self.user.is_active:
                raise forms.ValidationError('Акаунт заблокований')
        return self.cleaned_data

class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email*'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувача з таким email не знайдено')
        return email

from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({
            'placeholder': 'Текущий пароль*',
            'class': 'form-control'
        })
        self.fields['new_password1'].widget.attrs.update({
            'placeholder': 'Новый пароль*',
            'class': 'form-control'
        })
        self.fields['new_password2'].widget.attrs.update({
            'placeholder': 'Подтвердить пароль*',
            'class': 'form-control'
        })