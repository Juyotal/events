from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.edit import FormView


class RegisterPage(FormView):
    template_name = "accounts/register.html"
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('accounts:profile')

        return super(RegisterPage, self).get(*args, **kwargs)

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(
#                 request, f'{username}, Your account has been created! You are now able to log in')
#             return redirect('accounts:p')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileForm(request.POST)

        if p_form.is_valid():
            p_form.instance.user = request.user
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('main:events')

    else:
        p_form = ProfileForm()

    context = {
        'p_form': p_form
    }

    return render(request, 'accounts/profile.html', context)


def index(request):

    return render(request, 'accounts/index.html')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main:events')
