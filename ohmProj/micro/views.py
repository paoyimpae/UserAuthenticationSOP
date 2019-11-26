from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
import logging

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignupForm, EditProfileForm
from .tokens import account_activation_token
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('user.log')
file_handler.setFormatter(formatter)

# stream_handler = logger.StreamHandler()
# stream_handler.setFormatter(formatter)

# logger.addHandler(stream_handler)
logger.addHandler(file_handler)

from django.http import JsonResponse

def user_detail(request):
    data = {
                'username': request.user.username, 
                'firstName': request.user.first_name, 
                'lastName' : request.user.last_name,
                'email': request.user.email, 
                'telephone': request.user.telephone
            },
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = request.POST.get('username')
            email = request.POST.get('email')
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
            logger.info('Request for create user: {} - {}'.format(username, email))
            return HttpResponse('Please Confirm Your E-mail Address to Complete the Registration.')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


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
        username = request.POST.get('username')
        email = request.POST.get('email')
        login(request, user)
        logger.info('Activated User ID: {} - {}'.format(username, email))
        return render(request, 'registration/home.html')
    else:
        return HttpResponse('Activation Link is Invalid !')


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
        logger.info('Access to Login page: {}'.format(username))

    return render(request, template_name='micro/templates/registration/login.html', context=context)


def my_logout(request):
    logout(request)
    return redirect('login')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('registration:home'))
            # return render(request, template_name='/home.html')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        username = request.POST.get('username')
        logger.info('Access to Update Profile page: {}'.format(username))
        return render(request, 'registration/updateProfile.html', args)