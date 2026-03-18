from django import forms
from cities_light.models import Country, Region
from cabinet.models import User, Address


class RegisterPhysicalForm(forms.Form):
    # Особисті дані
    first_name = forms.CharField(max_length=50, label='ПІБ')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=13, label='Телефон')
    # Адреса
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False, label='Країна'
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False, label='Область'
    )
    city = forms.CharField(max_length=100, required=False, label='Місто')
    street = forms.CharField(max_length=255, required=False, label='Адреса')
    # Пароль
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Підтвердіть пароль')
    # Фото і ФОП
    image = forms.ImageField(required=False, label='Фото')
    is_fop = forms.BooleanField(required=False, label='Є ФОП')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email вже зареєстрований')
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Паролі не співпадають')
        return p2

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
        )
        if data.get('image'):
            user.image = data['image']
            user.save()
        return user


class RegisterLegalForm(forms.Form):
    # Контактні дані
    first_name = forms.CharField(max_length=50, label='ПІБ')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=13, label='Телефон')
    # Адреса фіз.
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False, label='Країна'
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False, label='Область'
    )
    city = forms.CharField(max_length=100, required=False, label='Місто')
    street = forms.CharField(max_length=255, required=False, label='Адреса')
    # Тип юр. особи
    legal_type = forms.ChoiceField(
        choices=[('legal', 'Юр. особа'), ('fop', 'ФОП')],
        label='Тип'
    )
    # Реквізити
    company_name = forms.CharField(max_length=200, required=False, label='Назва компанії')
    okpo = forms.CharField(max_length=10, required=False, label='ОКПО')
    edrpou = forms.CharField(max_length=10, required=False, label='ЄДРПОУ')
    # Юридична адреса
    legal_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False, label='Країна (юр.)'
    )
    legal_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False, label='Область (юр.)'
    )
    legal_city = forms.CharField(max_length=100, required=False, label='Місто (юр.)')
    legal_street = forms.CharField(max_length=255, required=False, label='Адреса (юр.)')
    legal_zip = forms.CharField(max_length=10, required=False, label='Індекс')
    # Пароль
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Підтвердіть пароль')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email вже зареєстрований')
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Паролі не співпадають')
        return p2

    def save(self):
        data = self.cleaned_data
        is_fop = data.get('legal_type') == 'fop'

        # Фізична адреса
        address = Address.objects.create(
            address_type=Address.TYPE_LEGAL,
            country=data.get('country'),
            region=data.get('region'),
            city=data.get('city', ''),
            street=data.get('street', ''),
            # Юридична адреса
            company_name=data.get('company_name', ''),
            edrpou=data.get('edrpou') if is_fop else None,
            okpo=data.get('okpo') if not is_fop else None,
            zip_code=data.get('legal_zip', ''),
        )
        user = User.objects.create_user(
            email=data['email'],
            password=data['password1'],
            first_name=data.get('first_name', ''),
            phone=data.get('phone', ''),
            is_fop=True,
            address=address,
        )
        return user