from django.urls import path

from . import views

app_name = "myapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("questions/", views.question_list, name="question_list"),
    path("questions/<int:question_id>/", views.question_detail, name="question_detail"),
    path("questions/<int:question_id>/results/", views.question_results, name="question_results"),
    path("questions/<int:question_id>/vote/", views.question_vote, name="question_vote"),
    path("question_create/", views.question_create, name="question_create"),
]