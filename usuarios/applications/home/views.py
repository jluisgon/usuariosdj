import datetime

from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin

# para redigirnos a una url las dos
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    TemplateView
)

# Create your views here.

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"
    # LoginRequiredMixin necesita de esta propiedad
    # indica que va a suceder que cuando intenten acceder a esta vista sin estar logeado
    login_url = reverse_lazy('users_app:user-login')


class FechaMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now() 
        return context
    
class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = 'home/mixin.html'