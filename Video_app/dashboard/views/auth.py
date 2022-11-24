# encoding:utf-8

from django.views.generic import View
from Video_app.lib.base_render import render_to_response
from django.shortcuts import redirect, reverse, render


class Login(View):
    TEMPLATES = 'dashboard/auth/Login.html'

    def get(self, request):
        return render_to_response(request, self.TEMPLATES)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)

        return redirect('login')
