from django.shortcuts import render
from django.views.generic import View


class Login(View):
    TEMPALTE = ''

    def get(self, request):
        return render(request, self.TEMPALTE)
