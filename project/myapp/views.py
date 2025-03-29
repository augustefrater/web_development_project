from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question
from .forms import QuestionForm


def index(request):
    context = {}
    return render(request, "myapp/index.html", context)


def question_list(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "myapp/question_list.html", context)


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "myapp/question_detail.html", {"question": question})


def question_results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "myapp/question_results.html", {"question": question})


def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "myapp/question_detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = selected_choice.votes + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("myapp:question_results", args=(question.id,)))

def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            Question.objects.create(
                question_text = form.cleaned_data["question_text"],
                pub_date = timezone.now()
            )
            return HttpResponseRedirect(reverse("myapp:question_list"))
    else:
        form = QuestionForm()

    context = {"form": form}
    return render(request, "myapp/question_create.html", context)