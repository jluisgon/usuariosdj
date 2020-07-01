from django.shortcuts import render

# import para envios de email
from django.core.mail import send_mail

# para redigirnos a una url las dos
from django.urls import reverse_lazy, reverse

# importar authenticate, que ya nos verifica la autentificacion
# importar login para que django mantenga activo ese username durante toda la sesion
# logout para salir de la sesion del usuario
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.mixins import LoginRequiredMixin

# HTTPResponseRedirect redireccionar dentro de un proceso
from django.http import HttpResponseRedirect

# View el padre de todas las vistas, solo recibe y ejecuta algo
from django.views.generic import (
    View
)


from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm
)

from .models import User

from .functions import code_generator

# Create your views here.


class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        # generamos el codigo de verificacion
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro = codigo            
        )
        # enviar el codigo al email del usuario
        asunto = 'confoirmacion de email'
        mensaje = 'Codigo de verificacion: ' + codigo
        email_remitente = 'email.com'
        # seguir el orden de parametros
        # [] --> pq se puede enviar a varios correos
        #send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        # redirigir a pantalla de validacion
        
        # se comenta ya que s va redirigir a otra pantalla
        #return super(UserRegisterView, self).form_valid(form)
        
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                # aqui se manda un parametro por HttpResponseRedirect a la url
                # puede ser pk o cualquier otro nombre del parametro
                kwargs = {'pk': usuario.id}
            )
        )

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    # nos lleva a la url co name panel en el etiqueta home_app (esta en la url de la app home)
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        # aqui ya se verifica que ese username y password ya existe en la BD y son correctos
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        # contexto self.request pq necesita a ese usuario asignarle a todo proyecto de la sesion actual 
        # con que usuario --> user
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):    
    
    def get(self, request,  *args, **kwargs):
        # del conexto request
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )
                        
class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm   
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        # recuperar el usuario que esta activo
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )              

        if user:
            newpassword=form.cleaned_data['password2'] 
            usuario.set_password(newpassword)
            usuario.save()
         
        # cierra sesion para que vuelva acceder al sistema    
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
    
    # como no depende de un modelo y solo va a recibir un formulario se trabaja con el FormView
class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm 
    success_url = reverse_lazy('users_app:user-login')
    
    # indicarle a la vista que envie un contexto con el pk que queremos recuperar en el form
    # sobreescribir esta funcion
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update ({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):     
        User.objects.filter(
            id = self.kwargs['pk']
        ).update(
            is_active = True
        )
        return super(CodeVerificationView, self).form_valid(form)
        
  
        
