from django.db import models

# Create your models here.

class Headline(models.Model):
	title = models.CharField(max_length=500)
	image = models.ImageField(blank=True, null=True)
	created_at  = models.DateField(auto_now_add=True)
	url = models.TextField()

	def __str__(self):
		return self.title
# 		