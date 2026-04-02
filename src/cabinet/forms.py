from django import forms
from cabinet.models import User


class RegularUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']




class FopUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'avatar']

    # Поля из Address
    company_name = forms.CharField(required=False, label='Назва компанії')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.address:
            self.fields['company_name'].initial = self.instance.address.company_name

    from django import forms
    from cabinet.models import User

    class RegularUserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']

        def save(self, commit=True):
            user = super().save(commit=False)

            # 👇 гарантированно сохраняем avatar
            if self.cleaned_data.get('avatar'):
                user.avatar = self.cleaned_data['avatar']

            if commit:
                user.save()

                if user.address:
                    user.address.company_name = self.cleaned_data.get('company_name',
                                                                      '')
                    user.address.save()

            return user

    class FopUserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['email', 'phone', 'avatar']

        # Поля из Address
        company_name = forms.CharField(required=False, label='Назва компанії')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.address:
                self.fields['company_name'].initial = self.instance.address.company_name

        def save(self, commit=True):
            user = super().save(commit=commit)
            if user.address:
                user.address.company_name = self.cleaned_data.get('company_name', '')
                user.address.save()
            return user