from django import forms
from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(forms.ModelForm):
    
    password1= forms.CharField(label='Password', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder':'Password'}
            )
        )

    password2= forms.CharField(label='Repeat Password', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder':'Repeat password'}
            )
        )

    class Meta:
        model= User
        fields= ('username','name','last_name', 'email', 'gender',)
        
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2','Password are not the same') # tambien se puede utilizar el raise
            
            # por hacer:
            # hacer que la contraseña tengo minimo 8 caracteres y maximo 20, que tengo catacteres especiales obligatorio.
        #if self.cleaned_data['password1'] > self.cleaned_data['password1']:
        

class LoginForm(forms.Form): # form.Form puedo hacer mi formulario a mi libertad sin depender del Model

    username= forms.CharField(label='Username', 
        required=True, 
        widget=forms.TextInput(
        attrs={'placeholder':'Username'}

        )
    )
    password= forms.CharField(label='Password', 
        required=True, 
        widget=forms.PasswordInput(
        attrs={'placeholder':'Password'}
            )
        )

    def clean(self):
        cleaned_data=super(LoginForm, self).clean()
        username= self.cleaned_data['username']
        password= self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('User data is not correct')
        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
    password1= forms.CharField(label='Current Password', 
        required=True, 
        widget=forms.PasswordInput(
        attrs={'placeholder':' Current Password'}
            )
        )
    password2= forms.CharField(label='New   Password', 
        required=True, 
        widget=forms.PasswordInput(
        attrs={'placeholder':'New Password'}
            )
        )
    """def clean(self):
        cleaned_data=super(UpdatePasswordForm, self).clean()
        password1= self.cleaned_data['password1']
        password2= self.cleaned_data['password2']

        if not authenticate(password1=password1, password2=password2):
            raise forms.ValidationError('Password is not correct')
        return self.cleaned_data"""

class VerificationForm(forms.Form):
    code_register = forms.CharField(required=True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user= pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    

    def clean_code_register(self):
        code= self.cleaned_data['code_register']  

        if len(code) == 6:
            # verificamos si el codigo y el id de usuario son validos:
            active= User.objects.code_validation(
                self.id_user, code)

            if not active:
                 raise forms.ValidationError('the code is not correct')
        else:
            raise forms.ValidationError('the code is not correct')
    
