from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from home.models import ChatUserData


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ChatUserData.objects.all().delete()
        context['tableheader'] = ['Username', 'Stupid', 'Fat', 'Dumb']
        context['data'] = {obj.username: {'username': obj.username, 'stupid': obj.stupid, 'fat': obj.fat,
                                          'dumb': obj.dumb} for obj in ChatUserData.objects.all().order_by('-id')}
        return context
