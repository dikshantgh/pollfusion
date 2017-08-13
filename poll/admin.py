from django.contrib import admin
from poll.models import Choice, Question, QuestionType
# Register your models here.


admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(QuestionType)
