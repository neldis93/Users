import datetime

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

# construir mixin
class DateMixin(object):
    def get_context_data(self, **kwargs):
        context = super(DateMixin, self).get_context_data(**kwargs)
        context['date']=datetime.datetime.now()
        return context


class HomePage(LoginRequiredMixin,TemplateView):
    template_name = "home/index.html"
    #LoginRequiredMixin
    login_url= reverse_lazy('users_app:user_logout')


class TemplateTestMixin(DateMixin,TemplateView):
    template_name='home/mixin.html'