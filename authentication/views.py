from django.shortcuts import render, redirect
from django.views import View
from validate_email import validate_email
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data
        print(email)
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'This email is already taken, please choose another one'}, status=409)

        return JsonResponse({'email_valid': True})
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data



        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'This username is already taken, choose another one'}, status=409)

        return JsonResponse({'username_valid': True})




class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        context = {
            'username': username,
            'email': email,

        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too Short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

                activate_url = 'http://'+domain+link


                emailmsg_subject = 'Activate Your Account'

                emailmsg_body = 'Hi '+user.username+'\n' +'Use This Link to Activate Your Account\n' + activate_url

                emailmsg = EmailMessage(
                    emailmsg_subject,
                    emailmsg_body,
                    "noreply@moneyapp.com",
                    [email],
                )

                emailmsg.send(fail_silently=False)

                messages.success(request, 'Account  Successfully Created, Check Your Email For Activation')
                return redirect('login')

        return render(request, 'authentication/register.html', context)

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.info(request, 'Account is Already Activated')
                return redirect('login')


            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated Successfully')
            return redirect('login')
        except Exception as ex:
            pass

        return redirect('login')







class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username+'. You Are Now Logged In')
                    return redirect('/')

                else:
                    messages.error(request, 'Account Is Not Active, Please Check Your Email')
                    return render(request, 'authentication/login.html')

            else:

                messages.error(request, 'Invalid Credentials, Try Again')
                return render(request, 'authentication/login.html')

        else:
            messages.error(request, 'Please Fill All Fields And Try Again')
            return render(request, 'authentication/login.html')




class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You Have Been Logged Out')
        return redirect('login')




