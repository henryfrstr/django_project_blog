from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from .token import account_activation_token
from .forms import RegistrationForm, UserEditForm
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from .forms import PwdChangeForm
from django.urls import reverse_lazy


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Details successfully updated!")
        else:
            messages.warning(request, "Enter a valid input")
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'users/profile_update.html',
                  {'user_form': user_form})


def register(request):

    form = RegistrationForm(request.POST or None)
    # form = UserCreationForm(request.POST or None)
    # print(form.is_valid())
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        subject = 'Activate your account'
        message = render_to_string(
            'users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        email_message = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
        )
        email_message.send(fail_silently=False)
        messages.success(request, 'Account successfully created')

        return redirect('login')

        # return HttpResponse('registered succesfully and activation sent')
        # form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('blog:home')
    else:
        return render(request, 'users/activation_invalid.html')


@login_required
def delete_user(request):

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('login')

    return render(request, 'users/delete.html')


class PasswordChange(PasswordChangeView):
    form_class = PwdChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'users/password_change_form.html'
