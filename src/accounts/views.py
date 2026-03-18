from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from cities_light.models import Country, Region
from .forms import RegisterPhysicalForm, RegisterLegalForm


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
            return redirect('/cabinet/')
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        user_type = request.POST.get('user_type')

        if user_type == 'physical':
            form = RegisterPhysicalForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/cabinet/')

            return render(request, self.template_name,
                         self.get_context(physical_form=form))

        elif user_type == 'legal':
            form = RegisterLegalForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/cabinet/')

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