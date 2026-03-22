from cabinet.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from cities_light.models import Country, Region
from .forms import RegisterPhysicalForm, RegisterLegalForm, LoginForm, CustomPasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import PasswordRecoveryForm
from .tasks import send_password_recovery_email, send_registration_email
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm



class RegisterView(View):
    template_name = 'accounts/reg-fiz.html'

    def get_context(self, physical_form=None, legal_form=None):
        return {
            'physical_form': physical_form or RegisterPhysicalForm(),
            'legal_form':    legal_form    or RegisterLegalForm(),
            'countries':     Country.objects.all(),
            'regions':       Region.objects.all(),
        }

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/cabinet/my_cabinet')
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        user_type = request.POST.get('user_type')

        if user_type == 'physical':
            form = RegisterPhysicalForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/cabinet/my_cabinet')

            return render(request, self.template_name,
                         self.get_context(physical_form=form))

        elif user_type == 'legal':
            form = RegisterLegalForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/cabinet/my_cabinet')

            return render(request, self.template_name,
                         self.get_context(legal_form=form))

        return redirect('accounts:register')

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('accounts:login')

    def post(self, request):
        logout(request)
        return redirect('accounts:login')

class LoginView(View):
    template_name = 'accounts/enter.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/cabinet/')
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            next_url = request.GET.get('next', '/cabinet/')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})

class PasswordRecoveryView(View):
    template_name = 'accounts/password-recovery.html'

    def get(self, request):
        return render(request, self.template_name, {
            'recovery_form': PasswordRecoveryForm()
        })

    def post(self, request):
        form = PasswordRecoveryForm(request.POST)
        if form.is_valid():
            from cabinet.models import User
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes

            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                f'/accounts/password-reset/{uid}/{token}/'
            )

            # Відправляємо в фоні через Celery
            send_password_recovery_email.delay(email, reset_url)

            return render(request, self.template_name, {
                'recovery_form': form,
                'success': True,
            })

        return render(request, self.template_name, {'recovery_form': form})

class PasswordResetConfirmView(View):
    template_name = 'accounts/password-recovery.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and default_token_generator.check_token(user, token):
            return render(request, self.template_name, {
                'uidb64': uidb64,
                'token': token,
                'valid': True,
            })
        return render(request, self.template_name, {'valid': False})

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and default_token_generator.check_token(user, token):
            p1 = request.POST.get('password1')
            p2 = request.POST.get('password2')
            if p1 and p1 == p2:
                user.set_password(p1)
                user.save()
                return redirect('accounts:login')

        return render(request, self.template_name, {'valid': False})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("cabinet:my_cabinet")



