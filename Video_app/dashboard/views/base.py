# encoding:utf-8
from django.views.generic import View
from Video_app.lib .base_render import render_to_response
from django.shortcuts import render


class Index(View):

    TEMPLATE = 'dashboard/Index.html'

    def get(self, request):
        return render_to_response(request, self.TEMPLATE)

