from django import forms
from cities_light.models import Country, Region, City
from .models import ClientOrder


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = ClientOrder
        fields = [
            "recipient_name",
            "phone",
            "email",
            "company",

            "delivery",

            "country",
            "region",
            "city",
            "delivery_address",
            "payment_method",
            "np_city_ref",
            "np_warehouse_ref",

            "comment",
        ]

        widgets = {
            'recipient_name': forms.TextInput(attrs={
                'placeholder': "Ім'я отримувача",
                'class': 'form-input'
            }),

            'phone': forms.TextInput(attrs={
                'placeholder': 'Телефон*',
                'class': 'form-input'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-input'
            }),

            'company': forms.TextInput(attrs={
                'placeholder': 'Компанія',
                'class': 'form-input'
            }),

            'delivery': forms.RadioSelect( ),
            'payment_method': forms.RadioSelect(),

            'country': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),

            'delivery_address': forms.TextInput(attrs={
                'placeholder': 'Вулиця, будинок, квартира',
                'class': 'form-input'
            }),

            'np_city_ref': forms.HiddenInput(),
            'np_warehouse_ref': forms.HiddenInput(),

            'comment': forms.Textarea(attrs={
                'placeholder': 'Коментар',
                'class': 'form-textarea'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # базові поля
        self.fields['recipient_name'].required = True
        self.fields['phone'].required = True

        # інші вимикаємо
        for field in self.fields.values():
            field.required = False