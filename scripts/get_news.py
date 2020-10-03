import os
import psycopg2
import requests as re
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

DATABASE_URL = "postgres://vapqwtuddvoocu:dc4fa7072cd240cba13b93e4e92ecff470e3bf075eab0b47b33232658417f0aa@ec2-107-22-7-9.compute-1.amazonaws.com:5432/dbu95qaiu69bq4"
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


# conn = psycopg2.connect(
# 					user = "news_owner",
#                     password = "siehf#$tc2.VTH34",
#                     database = "news_collector",
#                     host = "127.0.0.1",
#                     port = "5432",
#         )

cursor = conn.cursor()
# print(cursor)


sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=9)
def get_news():
		url = "https://indianexpress.com/section/india/"
		data = re.get(url)
		soup = BeautifulSoup(data.text, 'html.parser')
		# print(soup)
		News = soup.find_all('div', {"class":"articles"})
		# print(News)
		for artical in News:
			link = artical.find('a')['href']
			# image_src = artical.find('img')['src'].split()[0]
			try:
				image = artical.find('img')['data-lazy-src']
			except Exception as e:
				image = None
			# print(image_s)
			title = artical.find('h2').text
			# print(title)
			try:
				sql = "INSERT INTO news_headline(title, url, image, created_at) VALUES ('"+str(title)+"', '"+str(link)+"', '"+str(image)+"', now()) "
				cursor.execute(sql)
				conn.commit()	
			except psycopg2.errors.InFailedSqlTransaction:
				pass
			except psycopg2.errors.StringDataRightTruncation:
				pass 		

if __name__ == '__main__':
	sched.start()
	# get_news()




	
