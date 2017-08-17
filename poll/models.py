from django.db import models
import datetime
import django
from django.utils import timezone
# Create your models here.


class QuestionType(models.Model):

	# this is model for question type 
	topic = models.CharField(max_length=200)

	def __str__(self):

		return self.topic

class Question(models.Model):

	question_type = models.ForeignKey(QuestionType)
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField(default= django.utils.timezone.now)
	hit_ques = models.IntegerField(default =0)

	# def was_published_recently(self):
	# 	now = timezone.now()
	# 	return now - datetime.timedelta(days=1) <= self.pub_date <= now

	# 	#return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):

		return self.question_text


class Choice(models.Model):

	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	deleted = models.BooleanField(default=False)
	
	#def soft_del(self):
    #    self.deleted = True            
     #   self.save()

	
	def __str__(self):

		return self.choice_text

class Contact(models.Model):
	name = models.CharField(blank =True, max_length=100, help_text="enter name")
	address = models.CharField(blank =True, max_length=200, help_text="enter name")

	def __str__(self):
		return self.name