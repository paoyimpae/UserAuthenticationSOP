from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect

# Create your views here.
from micro.forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    args = {'form': form}
    return render(request, template_name='micro/register.html', context=args)


def home(request):
    return render(request, template_name='micro/home.html')


def my_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

            # next_url = request.POST.get('next_url')
            # if next_url:
            #     return redirect(next_url)
            # else:
            #     return redirect('index2')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'

    # next_url = request.GET.get('next')
    # if next_url:
    #     context['next_url'] = next_url

    return render(request, template_name='micro/login.html', context=context)


def my_logout(request):
    logout(request)
    return redirect('login')
