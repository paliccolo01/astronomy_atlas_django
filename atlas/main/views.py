from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Chapter, Subheading, Profile, Exam, Examlog, Question, Answer
from django.contrib.auth.forms import AuthenticationForm
from .forms import ExtendedUserCreationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"chapters": Chapter.objects.all})

def detail(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    return render(request,
                  template_name="main/detail.html",
                  context={"chapter": chapter})

def quiz(request):
    return render(request=request,
                  template_name="main/quiz.html",
                  context={"exams": Exam.objects.all})

def examdetail(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    equestions = [Question.objects.filter(id=exam_id)]
    eanswers = [Answer.objects.filter(id=exam_id)]

    return render(request,
                  template_name="main/examdetail.html",
                  context= {"exam": exam, "equestions": equestions, "eanswers": eanswers})

def quizdone(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    equestions = [Question.objects.filter(id=exam_id)]
    eanswers = [Answer.objects.filter(id=exam_id)]
    if request.method=="POST":
        postdatacollected=request.POST['choice']
        print (postdatacollected)

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('main:results', args=(question.id,)))

def results(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    return render(request, 'main/results.html', {'exam':exam})

def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid:
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, "New account created: {}".format(username))

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, "You are now logged in as: {}".format(username))

            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])


    form = ExtendedUserCreationForm()
    profile_form = ProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, "main/register.html", context)

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as: {}".format(username))
                return redirect("main:homepage")
            else:
                messages.info(request, "Invalid username or password")
        else:
            messages.info(request, "You did not fill out the form correctly!")


    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form":form})