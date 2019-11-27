from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
import logging

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignupForm, EditProfileForm
from .tokens import account_activation_token
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

import jwt, json
@login_required

def user_detail(request):
    payload = [{
                'username': request.user.username, 
                'firstName': request.user.first_name, 
                'lastName' : request.user.last_name,
                'email': request.user.email, 
                'telephone': request.user.telephone,
                'group': request.user.group,
            }]
    jwt_token = jwt.encode({'data':payload}, "SECRET_KEY", algorithm="HS256")

    data = {
                'username': request.user.username, 
                'firstName': request.user.first_name, 
                'lastName' : request.user.last_name,
                'email': request.user.email, 
                'telephone': request.user.telephone,
                'group': request.user.group,
                'token': str(jwt_token)
            }
    # print(jwt_token)

    # jwt_decode = jwt.decode(jwt_token, "SECRET_KEY", "[HS256]")
    # username = jwt_decode['username']

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

# def user_detail(request):
#     data = [{
#                 'username': request.user.username, 
#                 'firstName': request.user.first_name, 
#                 'lastName' : request.user.last_name,
#                 'email': request.user.email, 
#                 'telephone': request.user.telephone,
#                 'group': request.user.group,
#             }],
#     jwt_token = jwt.encode({{data:data}}, "SECRET_KEY", algorithm="HS256")
#     # print(jwt_token)

#     # jwt_decode = jwt.decode(jwt_token, "SECRET_KEY", "[HS256]")
#     #
#     # username = jwt_decode['username']

#     return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
# def user_detail(request):
#     data = {
#                 'username': request.user.username, 
#                 'firstName': request.user.first_name, 
#                 'lastName' : request.user.last_name,
#                 'email': request.user.email, 
#                 'telephone': request.user.telephone,
#                 'group': request.user.group,
#                 'token': account_activation_token.make_token(request.user)
#             },
#     return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            if form.cleaned_data.get('group') != '---------':
                group = Group.objects.get(name=form.cleaned_data.get('group'))
                user.groups.add(group)
                user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            # return HttpResponse('Please Confirm Your E-mail Address to Complete the Registration.')
            return render(request, 'registration/confirmation.html')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def confirmation(request):
    return render(request, 'registration/confirmation.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/home.html')
    else:
        # return HttpResponse('Activation Link is Invalid !')
        return render(request, 'registration/invalid.html')

def invalid(request):
    return render(request, 'registration/invalid.html')

@login_required
def home(request):
    return render(request, template_name='registration/home.html')


def my_login(request):
    context = {}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                home(request)

                # next_url = request.POST.get('next_url')
                # if next_url:
                #     return redirect(next_url)
                # else:
                #     return redirect('index2')
            else:
                context['username'] = username
                context['password'] = password
                context['error'] = 'Wrong Username or Password !'

        # next_url = request.GET.get('next')
        # if next_url:
        #     context['next_url'] = next_url
        username = request.POST.get('username')
        email = request.POST.get('email')

    return render(request, template_name='micro/templates/registration/login.html', context=context)

@login_required
def my_logout(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse_lazy('registration:home'))
            return render(request, template_name='registration/home.html')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        username = request.POST.get('username')
        return render(request, 'registration/updateProfile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, 'registration/home.html')
        else:
            return redirect(reverse('registration:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'registration/change_password.html', args)