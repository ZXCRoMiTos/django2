from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authapp.forms import ShopUserLoginForm, ShopUserCreationForm, ShopUserChangeForm
from authapp.models import ShopUser


def login(request):
    redirect_to = request.GET.get('next', '')
    message = ''

    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            redirect_to = request.POST.get('redirect-to')
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_activate:
                    auth.login(request, user)
                    return HttpResponseRedirect(redirect_to or reverse('main:index'))
                else:
                    message = 'Активируйте пользователя!'
    else:
        form = ShopUserLoginForm()

    context = {
        'page_title': 'логин',
        'form': form,
        'redirect_to': redirect_to,
        'message': message,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    registered = False

    if request.method == 'POST':
        form = ShopUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if user.send_verify_mail():
                registered = True
            else:
                print('Ошибка отправки.')
    else:
        form = ShopUserCreationForm()

    context = {
        'page_title': 'регистрация',
        'form': form,
        'registered': registered,
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        form = ShopUserChangeForm(request.POST, request.FILES,
                                  instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserChangeForm(instance=request.user)

    context = {
        'page_title': 'редактирование',
        'form': form,
    }
    return render(request, 'authapp/update.html', context)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_valid_key():
            user.is_activate = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))

