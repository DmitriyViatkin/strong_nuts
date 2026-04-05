from django import forms
from cities_light.models import Country, Region
from django.contrib.auth.models import AbstractUser

from cabinet.models import User, Address


class RegularUserForm(forms.ModelForm):
    full_name = forms.CharField(
        required=False,
        label='ПІБ',
        help_text='Прізвище Ім\'я По батькові'
    )
    class Meta:
        model = User
        fields = [  'email', 'phone', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        isinstance= kwargs.get('instance')
        if self.instance:
            if isinstance:
               parts = filter(None, [
                   isinstance.last_name,
                   isinstance.first_name,
                   isinstance.second_name
               ])
            self.fields['full_name'].initial = ' '.join(parts)

    def save(self, commit=True):
        user = super().save(commit=False)

        full_name = self.cleaned_data.get('full_name', '').strip()
        parts = full_name.split()

        user.last_name = parts[0] if len(parts) > 0 else ''
        user.first_name = parts[1] if len(parts) > 1 else ''
        user.second_name = parts[2] if len(parts) > 2 else ''

        if commit:
            user.save()
        return user


class FopUserForm(forms.ModelForm):
    company_name = forms.CharField(required=False, label='Назва компанії')

    class Meta:
        model = User
        fields = ['email', 'phone', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Підтягуємо початкове значення company_name з адреси
        if self.instance and self.instance.address:
            self.fields['company_name'].initial = self.instance.address.company_name

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.address:
                user.address.company_name = self.cleaned_data.get('company_name', '')
                user.address.save()
        return user


class AddressForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label='Країна',
        widget=forms.Select(attrs={'placeholder': 'Країна', 'id': 'id_country'})
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        empty_label='Область',
        widget=forms.Select(attrs={'placeholder': 'Область', 'id': 'id_region'})
    )

    class Meta:
        model = Address
        fields = ['country', 'region', 'city', 'street', 'zip_code', 'company_name', 'edrpou', 'pdv']
        widgets = {
            'city': forms.TextInput(attrs={'placeholder': 'Місто*', 'required': True}),
            'street': forms.TextInput(attrs={'placeholder': 'Вулиця'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Індекс'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Назва компанії'}),
            'edrpou': forms.TextInput(attrs={'placeholder': 'ЄДРПОУ'}),
            'pdv': forms.TextInput(attrs={'placeholder': 'ПДВ'}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.country:
                self.fields['region'].queryset = Region.objects.filter(
                    country=self.instance.country
                )


                if not self.data:
                    self.initial['country'] = self.instance.country.pk
                    if self.instance.region:
                        self.initial['region'] = self.instance.region.pk
            else:
                self.fields['region'].queryset = Region.objects.none()