

# import models
from django.db import models

# import necesario para la admnisracion de usuarios
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    
     # is_staff --> si este usuario puede o no acceder al adm de Django
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,            
            **extra_fields
        )
        # se necesita que el password se encripte
        user.set_password(password)
        # using --> hace referencia con que bd vamos a trabajar 
        user.save(using=self.db)
        return user      
              
    # se llama cuando se crea un usuario
    def create_user (self, username,  email, password=None, **extra_fields):
        return self._create_user(username,  email, password, False, False, **extra_fields)
    
    # desde la terminal
    def create_superuser(self, username, email, password=None, **extra_fields):
        # funcion que esta dentro de BaseUserManager y que es privada
        # es privada para que solo esa utiliza desde esta funcion en especifico (create_superuser)
        # o desde la terminal
        return self._create_user(username, email, password, True, True, **extra_fields)
    

