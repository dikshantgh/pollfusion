from django.db import models
from datetime import datetime
# Create your models here.


class QuestionType(models.Model):

	# this is model for question type 
	topic = models.CharField(max_length=200)

	def __str__(self):

		return self.topic

class Question(models.Model):

	question_type = models.ForeignKey(QuestionType)
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField(default=datetime.now)
	hit_ques = models.IntegerField(default =0)

	def __str__(self):

		return self.question_text


class Choice(models.Model):

	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	

	def __str__(self):

		return self.choice_text