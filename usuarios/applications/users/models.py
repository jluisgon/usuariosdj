from django.db import models

# se importa que se va hereder del AbstractBaseUser
#si hablamos de usuario siempre vamos a importar de from django.contrib.auth
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin 

# importar managers
from .managers import UserManager

# Create your models here.

# hereda de AbstractBaseUser
# PermissionsMixin --> 
class User(AbstractBaseUser, PermissionsMixin):
   
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )
    
    username = models.CharField(max_length=10, unique= True)
    email = models.EmailField()
    nombres = models.CharField(max_length=30,  blank = True)
    apellidos = models.CharField(max_length=30,  blank = True)
    genero = models.CharField(max_length=1, choices = GENDER_CHOICES,  blank = True)
    # campos para solicitados para crear usuarios
    is_staff = models.BooleanField(default = False)
    
    
    # usuario que va a servir para autentificar en el login del Admin de Django    
    USERNAME_FIELD = 'username'
    # para campos requeridos al crear usuarios
    REQUIRED_FIELDS = ['email',]
    
    objects = UserManager()

    # sobreescribiendo otras funciones
    def get_short_name(self):
        return self.username
    
    # es como el __str__, pero el __str__ es mas utilizado
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos
    
    