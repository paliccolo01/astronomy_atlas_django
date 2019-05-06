from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Chapter, Subheading, Profile, Exam, Examlog, Question, Answer
from django.contrib.auth.forms import AuthenticationForm
from .forms import ExtendedUserCreationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse


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
    if request.user.is_authenticated:
        return render(request=request,
                      template_name="main/quiz.html",
                      context={"exams": Exam.objects.all})
    else:
        messages.info(request, "Please login first!")
        return redirect("main:login")

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

    #equestionscounter = Question.objects.filter(id=exam_id).count(Question.id)
    #print("ennyi kerdes volt osszesen: " + str(equestionscounter))

    total_good_answers = 0
    quizsuccess = False
    quizgoal = exam.goal
    if request.method == "POST":
        #using list comprehension:
        for score_key in [key for key in request.POST.keys() if key.startswith('choice[')]:
            #print("score_key: " + str(score_key))
            myvar = request.POST.get(score_key)
            #print("myvar: " + str(myvar))
            if myvar == "True":
                total_good_answers += 1

        if exam.goal <= total_good_answers:
            quizsuccess = True
        else:
            quizsuccess = False

        request.session['total_good_answers'] = total_good_answers
        request.session['quizgoal'] = quizgoal
        request.session['quizsuccess'] = quizsuccess
        #print("nyertel, mert a cel: " + str(exam.goal) +" es ennyi pontod lett: " + str(total_good_answers))
        current_user = request.user
        examlog = Examlog()
        examlog.exam = exam
        examlog.participant = current_user
        examlog.achieved = total_good_answers
        examlog.passed = quizsuccess
        examlog.attempt += 1
        examlog.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('main:results', args=(exam_id,)))

def results(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    total_good_answers = request.session['total_good_answers']
    quizgoal = request.session['quizgoal']
    quizsuccess = request.session['quizsuccess']
    return render(request, 'main/results.html', {'exam':exam, 'total_good_answers':total_good_answers, 'quizgoal':quizgoal, 'quizsuccess':quizsuccess,})

def account(request):
    return HttpResponse("This is the account page")


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