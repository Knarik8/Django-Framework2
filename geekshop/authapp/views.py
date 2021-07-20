from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView, LogoutView

from .models import ShopUser


class Login(LoginView):
    model=ShopUser
    form_class = ShopUserLoginForm
    template_name = 'authapp/login.html'


# def login(request):
#     title = 'вход'
#
#     login_form = ShopUserLoginForm(data=request.POST)
#     next = request.GET['next'] if 'next' in request.GET.keys() else ''
#     if request.method == 'POST' and login_form.is_valid():
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username, password=password)
#         if user and user.is_active:
#             auth.login(request, user)
#             if 'next' in request.POST.keys():
#                 return HttpResponseRedirect(request.POST['next'])
#             else:
#                 return HttpResponseRedirect(reverse('index'))
#
#     context = {
#         'title': title,
#         'login_form': login_form,
#         'next': next,
#     }
#     return render(request, 'authapp/login.html', context=context)


class Logout(LogoutView):
    template_name = 'geekshop/index.html'


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


# class Register(CreateView):
#     model = ShopUser
#     template_name = 'authapp/register.html'
#     form_class = ShopUserRegisterForm
#
#
#     def get_success_url(self):
#         return reverse('auth:login')


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            send_verify_link(user)
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


# class Edit(UpdateView):
#     model = ShopUser
#     template_name = 'authapp/edit.html'
#     form_class = ShopUserRegisterForm




def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        photo_50 = get_object_or_404(ShopUser.avatar)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}

    return render(request, 'authapp/edit.html', content)


def send_verify_link(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'Your link for account activation:{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, key):
    user = ShopUser.objects.filter(email=email).first()
    if user and user.activation_key == key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.activation_key_created = None
        user.save()
        auth.login(request, user)
    return render(request, 'authapp/verify.html')