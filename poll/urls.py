from django.conf.urls import url
from poll import views

app_name ='poll'
urlpatterns = [
    url(r"^$", views.QuestionTypeView.as_view(), name="main_page"),
    url(r"^questions/(?P<pk>\d+)/$", views.QuestionBriefView.as_view(), name="question_list"),
    url(r"^option/(?P<pk>\d+)/$", views.QuestionDetailView.as_view(), name="question_detail"),
    url(r"^type/$", views.TypeCreateView.as_view(), name="create_type"),
    url(r"^createquestion/(?P<pk>\d+)/$", views.QuestionCreateView.as_view(), name="create_question"),
    url(r"^createoption/(?P<pk>\d+)/$", views.OptionCreateView.as_view(), name="create_option"),





]
