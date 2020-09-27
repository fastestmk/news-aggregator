from django.shortcuts import render, redirect
import requests as re
from bs4 import BeautifulSoup 
from .models import *
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class NewsList(TemplateView):
	template = "news/home.html"
	def get(self, request):
		if request.user.is_authenticated:			
			headlines = Headline.objects.all()[::-1]
			# page = request.GET.get('page', 1)
			# paginator = Paginator(headlines, 9)
			# try:
			# 	news = paginator.page(page)
			# except PageNotAnInteger:
			# 	news = paginator.page(1)
			# except EmptyPage:
			# 	news = paginator.page(paginator.num_pages)		
			context = {'object_list': headlines}
			return render(request, self.template, context)
		
		return redirect('signin')	


class ScrapeNews(View):
	# template = "news/news.html"
	def get(self, request):
		url = "https://indianexpress.com/section/world/"
		data = re.get(url)
		soup = BeautifulSoup(data.text, 'html.parser')
		# print(soup)
		News = soup.find_all('div', {"class":"articles"})
		# print(News)
		for artical in News:
		    link = artical.find('a')['href']
		    # image_src = artical.find('img')['src'].split()[0]
		    image_src = artical.find('img')['data-lazy-src']
		    print(image_src)
		    title = artical.find('h2').text
		    new_headline = Headline()
		    new_headline.title = title
		    new_headline.url = link
		    new_headline.image = image_src
		    new_headline.save()

		return redirect("home")    
		# return redirect("../")
		# print(soup)
		# return render(request, local())


class SignUpView(TemplateView):
	template = 'news/signup.html'
	def get(self, request):
		return render(request, self.template, locals())
	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		print(request.POST)
		try:
			user = User.objects.get(username=username)
			messages.error(request, 'This user already exists')
			return redirect('signup')
		except User.DoesNotExist:
			user = User.objects.create_user(
				username = username,
				password=password
			)
			user.save()
			print(user)
			messages.success(request, 'Thank you for signup, Please confirm your mail or do it later')
			return redirect('signin')
		except Exception as e:
			if user:
				user.delete(	)
			messages.error(request, "Something wrong happend please try again")
			return redirect('signup')	


class LoginView(TemplateView):
	template = 'news/signin.html'
	context = {}
	def get(self, request,*args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		return render(request, self.template, locals())
	def post(self, request,*args,**kwargs):
		username = request.POST.get('user')
		password = request.POST.get('password')	
		try:
			user = User.objects.get(username=username)	
			userauth = authenticate(username=username, password=password)
			if userauth:
				login(request, user,backend='django.contrib.auth.backends.ModelBackend')
				return redirect("home")		
			else:
				messages.info(request, 'Password is not correct')	
		except User.DoesNotExist as e:
			messages.info(request, "User doesn't exist")
		return redirect("signin")

def LogoutView(request):	
	logout(request)
	return redirect('signin')
