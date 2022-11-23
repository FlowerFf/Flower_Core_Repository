from django.shortcuts import render
from django.views.generic import View


class Login(View):
    TEMPLATES = ''

    def get(self, request):
        return render(request, self.TEMPLATES)
