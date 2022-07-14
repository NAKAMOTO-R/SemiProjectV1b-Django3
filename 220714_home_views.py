import random

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from movies.models import Movie
from accounts.models import User
# Create your views here.

class HomeView(View):
    def get(self, request):
        random_movies = []
        movies = Movie.objects.order_by('-popularity')

        random_movies.sort()

        random_nums = random.sample(range(0, len(movies)), 12)
        random_nums.sort()

        for i in random_nums:
            random_movies.append(movies[i])

        context = {'movies': random_movies}
        return render(request, 'home.html', context)

    def post(self, request):
        pass

class LoginView(View):

    def post(self, request):
        form = request.POST.dict()

        isExisted = User.objects.filter(username=form['userid'], password=form['passwd']).exists()

        # if count == 1:
        if isExisted:    # 로그인 성공시
            user = User.objects.get(username=form['userid'])
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            returnPage = '/'
        else:
            returnPage = '/loginfail'

        return redirect(returnPage)

class LoginfailView(View):
    def get(self, request):
        return render(request, 'loginfail.html')



class LogoutView(View):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.delete()
            auth_logout(request)
        return redirect('home')
