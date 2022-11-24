# encoding:utf-8

from django.views.generic import View
from Video_app.lib import base_render
from django.shortcuts import render


class Base(View):

    TEMPLATE = '/templates/dashboard/Nav.html'

    def get(self, request):
        return render(request, self.TEMPLATE)

