import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Test, Result
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def index(request):
    tests = Test.objects.all()
    return render(request, 'tests/index.html', {'tests': tests})


def site_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('index')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    return render(request, 'tests/register.html', {})


def site_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'tests/login.html', {})


def site_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')


def lk(request):
    user = request.user
    return render(request, 'tests/lk.html', {'user': user})


def test(request, id):
    if request.user.is_authenticated:
        test = Test.objects.get(pk=id)
        return render(request, 'tests/test.html', {'test': test})
    else:
        return redirect('index')


def start_test(request, id):
    if request.user.is_authenticated:
        test = Test.objects.get(pk=id)
        question = test.question_set.first()
        request.session['test'] = test.id
        request.session['checkpoint'] = question.id
        request.session['answers'] = {}
        return redirect('question', test_id=test.id, question_id=question.id)
    else:
        return redirect('index')


def question(request, test_id, question_id):
    if request.user.is_authenticated:
        if int(request.session['checkpoint']) == int(question_id):
            test = Test.objects.get(pk=test_id)
            question = test.question_set.get(pk=question_id)
            right_answers_count = question.answer_set.filter(right=True).count()
            if request.method == 'POST':
                this_question_id = int(request.POST['this_question_id'])
                this_question_answer = request.POST.getlist('answer')
                answers = request.session['answers']
                answers[str(this_question_id)] = this_question_answer
                request.session['answers'] = answers
                if this_question_id == test.question_set.last().id:
                    id = resultmaker(request)
                    return redirect('result', id=id)
                else:
                    question = test.question_set.get(pk=this_question_id+1)
                    request.session['checkpoint'] = question.id
                    return redirect('question', test_id=test.id, question_id=question.id)
            return render(request, 'tests/question.html', {'test': test, 'question': question, 'right_answers_count': right_answers_count})
        else:
            test = Test.objects.get(pk=test_id)
            question = test.question_set.get(pk=int(request.session['checkpoint']))
            return redirect('question', test_id=test.id, question_id=question.id)
    else:
        return redirect('index')


def resultmaker(request):
    if request.user.is_authenticated:
        test = Test.objects.get(pk=int(request.session['test']))
        user = request.user
        answers = request.session['answers']
        right_count = 0
        for k, v in answers.items():
            right_answers = [i.text for i in test.question_set.get(pk=k).answer_set.filter(right=True)]
            if v == right_answers:
                right_count += 1
        percent = right_count/test.question_set.count()*100
        result = Result()
        result.test = test
        result.user = user
        result.answers = str(answers).replace("'",'"')
        result.percent = percent
        result.save()
        return result.id
    else:
        return redirect('index')


def result(request, id):
    if request.user.is_authenticated:
        result = Result.objects.get(pk=id)
        answers = json.loads(result.answers).items()
        right_count = 0
        for k, v in answers:
            right_answers = [i.text for i in result.test.question_set.get(pk=k).answer_set.filter(right=True)]
            if v == right_answers:
                right_count += 1
        not_right_count = result.test.question_set.count()-right_count
        if result.user == request.user:
            return render(request, 'tests/result.html', {'result': result, 'answers': answers, 'right': right_count, 'not_right': not_right_count})
        else:
            return redirect('index')
    else:
        return redirect('index')

