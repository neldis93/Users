from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .models import User
from .forms import UserRegisterForm,LoginForm, UpdatePasswordForm, VerificationForm
from .functions import code_generator


class UserRegisterView(FormView):
    template_name='users/register.html'
    form_class= UserRegisterForm
    success_url='/'

    def form_valid(self,form):
        # generar el codigo
        code= code_generator()
        #
        #form.cleaned_data recupaerar lo que nos envia el formulario(forms.py, los fields)
        user= User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            #**extra_fields
            name=form.cleaned_data['name'],
            last_name= form.cleaned_data['last_name'],
            gender=form.cleaned_data['gender'],
            code_register= code,
        ) 
        # enviar el codigo al email del user
        affair='Email Confirmation'
        message='Verefication Code: ' + code
        sender_email= 'neldis12@hotmail.com'

        send_mail(affair,message,sender_email, [form.cleaned_data['email']]) # 'email' viene del models.py
        
        #redirigir a pantalla de validacion
        return HttpResponseRedirect(reverse('users_app:user_verification', kwargs={'pk':user.id} )) # el user de arriba
        #return super(UserRegisterView, self).form_valid(form)


class LoginUserView(FormView):
    template_name='users/login.html'
    form_class= LoginForm
    success_url= reverse_lazy('home_app:panel')

    def form_valid(self,form):
        user= authenticate(
            username=form.cleaned_data['username'], 
            password= form.cleaned_data['password']
        )
        login(self.request,user)
        return super(LoginUserView, self).form_valid(form)      


class LogoutView(View):

    def get(self,request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('users_app:user_login'))    

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name= 'users/update.html'
    form_class= UpdatePasswordForm
    success_url= reverse_lazy('users_app:user_login')
    # para que no acceda cuando cierre sesion a la url de update
    login_url= reverse_lazy('users_app:user_login')

    def form_valid(self, form):
        user_active= self.request.user # recuperar el ususario activo
        user= authenticate(
            username=user_active.username, 
            password= form.cleaned_data['password1']
        )

        if user:
            new_password= form.cleaned_data['password2']
            user_active.set_password(new_password)
            user_active.save()

        logout(self.request) 

        return super(UpdatePasswordView,self).form_valid(form)


class CodeVerificationView(FormView):
    template_name='users/verification.html'
    form_class= VerificationForm
    success_url=reverse_lazy('users_app:user_login')

    def get_form_kwargs(self):
        kwargs= super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs['pk']})

        return kwargs

    def form_valid(self,form):

        User.objects.filter(
            id= self.kwargs['pk']
        ).update(is_active=True)
        
        return super(CodeVerificationView, self).form_valid(form)