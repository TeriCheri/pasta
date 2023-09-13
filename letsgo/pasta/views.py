from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5] 
    template = loader.get_template("pasta/index.html")
    context = {
        "latest_question_list": lastest_question_list
        }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "pasta/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id) 
    return render(request, "pasta/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
    
        return render(request, "pasta/detail.html",
                  {
                      "question": question,
                      "error_message": "You didn't select a choice.",
                    },
                  )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("pasta:results", args=(question.id,)))


class IndexView(generic.ListView):
    template_name = "pasta/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions (not includint those set to be published in the future)."""
        return Question.objects.filter(pub_date_lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "pasta/detail.html"
    def get_queryset(self):            
        """
        Excludes any questions that aren't published yeet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "pasta/results.html"


# Create your views here.
