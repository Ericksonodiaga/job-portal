from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from accounts.forms import *
from accounts.models import *
from accounts import utils
from jobosoft.permission import user_is_employee
from datetime import datetime, timedelta
from django.db import IntegrityError
from django.utils import timezone


def get_success_url(request):
   
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('jobosoft:home')


def employee_registration(request):
   
    form = EmployeeRegistrationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form = form.save()
        return redirect('accounts:login')
    context = {
        'form': form
    }

    return render(request, 'accounts/employee-registration.html', context)


def employer_registration(request):
    

    form = EmployerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('accounts:login')

    context = {
        'form': form
    }

    return render(request, 'accounts/employer-registration.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_employee
def employee_edit_profile(request, id=id):
   
    if request.method == "POST":
        form = EmployeeProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form = form.save()
            messages.success(request, 'Your Profile Was Successfully Updated!')
            return redirect(reverse("accounts:edit-profile", kwargs={
                'id': form.id
            }))

        context = {
            'form': form
        }
        return render(request, 'accounts/employee-edit-profile.html', context)

    elif request.method == "GET":
        form = EmployeeProfileEditForm(instance=request.user)

        context = {
            'form': form
        }
        return render(request, 'accounts/employee-edit-profile.html', context)


def user_logIn(request):
    

    form = UserLoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('/')

    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        'form': form,
    }

    return render(request, 'accounts/login.html', context)


def user_logOut(request):
   
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('accounts:login')


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except Exception:
            messages.error(request, "Invalid Email")
            return render(request, 'accounts/reset_password.html')

        # prevent same user from creating multiple entries
        try:
            existing = OTPModel.objects.get(user=user)
            existing.delete()
        except Exception:
            pass

        # user created buy social has no phone number
        if not user.phone_number or user.phone_number == "":
            messages.error(request, "User has no phone number")
            return redirect('accounts:login')

        # send a text message to that user and generate otp code
        otp_model = OTPModel()
        while True:
            otp_model.otp_code = utils.generate_code(8)
            otp_model.user = user
            otp_model.UUID = utils.generate_code(50)
            otp_model.expiry = datetime.now() + timedelta(minutes=30)

            try:
                otp_model.save()
                break
            except IntegrityError:
                continue
        response = utils.send_sms(otp_model.otp_code, user.phone_number)
        print(response)
        messages.info(request, f"Code set to your phone number {utils.blur_phone_number(user.phone_number)}")
        return redirect('accounts:reset_otp')

    return render(request, 'accounts/reset_password.html')


def otp_confirmation(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        if not otp:
            return HttpResponseBadRequest()

        try:
            otp_model = OTPModel.objects.get(otp_code=otp)
            if otp_model.expiry < timezone.now():
                otp_model.delete()
                messages.error(request, "OTP code expired")
                return redirect('accounts:reset_change')

            return redirect('accounts:reset_change', otp_model.UUID)
        except Exception as e:
            print(e)
            messages.error(request, "Invalid otp")
            return render(request, "accounts/enter_otp.html")

    return render(request, "accounts/enter_otp.html")


def change_password(request, UUID):
    try:
        otp_model = OTPModel.objects.get(UUID=UUID)
    except Exception:
        return redirect('accounts:login')

    if request.method == "POST":
        pswd1 = request.POST.get("pswd")
        pswd2 = request.POST.get("pswd2")

        if not pswd1 == pswd2:
            messages.error(request, "Passwords Do Not Match")
            return redirect('accounts:reset_change', UUID)

        user = otp_model.user
        user.set_password(pswd1)
        user.save()

        otp_model.delete()

        return redirect("accounts:login")

    return render(request, "accounts/change_password.html")
