from django.shortcuts import render, redirect
import requests as re
from bs4 import BeautifulSoup 
from .models import *
from django.views.generic import TemplateView, View

# Create your views here.

class NewsList(TemplateView):
	template = "news/home.html"
	def get(self, request):
		headlines = Headline.objects.all()[::-1]
		context = {'object_list': headlines}
		return render(request, self.template, context)


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

# News = soup.find_all('div', {"class":"curation-module__item"})
# 		print(News)
# 		for artcile in News:
# 		    main = artcile.find_all('a')[0]
# 		    link = main['href']
# 		    image_src = str(main.find('img')['srcset']).split(" ")[-4]
# 		    title = main['title']
# 		    new_headline = Headline()
# 		    new_headline.title = title
# 		    new_headline.url = link
# 		    new_headline.image = image_src
# 		    new_headline.save()
# 		    print("-----------------",new_headline)		