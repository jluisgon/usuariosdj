from django import forms

from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(forms.ModelForm):
    """Form definition for MODELNAME."""

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña'
            }
        )
    )

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero'
        )

    # validar que el password sea igual al de repetir
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            # poner el error en el campo del formulario
            self.add_error('password2', 'Las contraseñas no son iguales')

 # como no dependemos de un modelo , usamos la herencia de forms.Form
class LoginForm(forms.Form):

    username = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username',
                'style': '{margin: 10px}',
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    # asi indica a Django que es una de las primeras validaciones a aplicar
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if not authenticate (username = username , password = password):
            raise forms.ValidationError('Los datos del usuario no son corretos')
        
        # devuelve todos los datos
        return  self.cleaned_data
    

class UpdatePasswordForm(forms.Form):
    
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Atual'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )


class VerificationForm(forms.Form):
    codregistro = forms.CharField(required= True)
    
    # con esto le indicamos al formulario que estamos recibiendo algo contexto o kwargs de nuestra vista
    # __init__ se ejecuta al momento de iniciar el formulario    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    
    
    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']
        
        if len(codigo) == 6:
            # verificamos que el codigo de verificacion y el id de usuario son validos
            activo = User.objects.Cod_valitation(
                self.id_user,
                codigo
            )
            if not activo:
               raise forms.ValidationError('El codigo es incorrecto')   
        else:
            raise forms.ValidationError('El codigo es incorrecto')    