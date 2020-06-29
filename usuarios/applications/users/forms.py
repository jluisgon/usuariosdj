from django import forms

from .models import User

class UserRegisterForm(forms.ModelForm):
    """Form definition for MODELNAME."""
    
    password1 = forms.CharField(
         label = 'Contraseña',
         required= True,
         widget = forms.PasswordInput(
             attrs = {
                 'placeholder' : 'Contraseña'
             }
        )         
    )    
    password2 = forms.CharField(
         label = 'Contraseña',
         required= True,
         widget = forms.PasswordInput(
             attrs = {
                 'placeholder' : 'Repetir Contraseña'
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
        
        
