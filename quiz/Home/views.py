from .models import *
from django.shortcuts import render, redirect
import random
from django.contrib.auth.decorators import login_required
from .models import QuizResult
from django.contrib import messages
from django.db.models import Avg, Count
from django.core.mail import send_mail 
from django.conf import settings

# Index/Home Page
@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'pages/index.html')

# Rules Page
@login_required(login_url='/accounts/login/')
def rules_page(request, subject):
    return render(request, 'pages/rules.html', {'subject': subject})

# Start Quiz Based on Subject
@login_required(login_url='/accounts/login/')
def start_quiz(request, subject):
    if request.method == 'POST' and request.POST.get('agree'):
        return redirect('quiz', subject=subject)
    return redirect('rules_page', subject=subject)

# Quiz View with Multi-Attempt Support
@login_required(login_url='/accounts/login/')
def quiz_view(request, subject):
    if subject == "java":
        QuestionModel = JavaQuestion
    elif subject == "cpp":
        QuestionModel = CppQuestion
    elif subject == "python":
        QuestionModel = PythonQuestion 
    else:
        return redirect('index')

    if request.method == "GET":
        just_completed = request.session.pop(f"{subject}_just_completed", False)
        if just_completed:
            latest_result = QuizResult.objects.filter(user=request.user, subject=subject).order_by('-id').first()
            if latest_result:
                percentage = round((latest_result.score / 10) * 100, 2)
                return render(request, "quiz/result.html", {
                    'score': latest_result.score,
                    'correct': latest_result.score,
                    'wrong': 10 - latest_result.score,
                    'total': 10,
                    'percentage': percentage,
                    'subject': subject.capitalize(),
                    'error_message': ""
                })

        # Show quiz questions
        questions = list(QuestionModel.objects.order_by('?')[:10])
        for q in questions:
            q.options = [q.option1, q.option2, q.option3, q.option4]

        subject_template_map = {
            'java': 'quiz/java.html',
            'cpp': 'quiz/cpp.html',
            'python': 'quiz/python.html'
        }

        template_name = subject_template_map.get(subject)
        if not template_name:
            return redirect('index')

        return render(request, template_name, {
            'questions': questions,
            'subject': subject
        })

    elif request.method == "POST":
        correct = wrong = 0

        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                continue
            try:
                question = QuestionModel.objects.get(pk=key)
                selected = request.POST[key]
                if selected == question.correct_answer:
                    correct += 1
                else:
                    wrong += 1
            except QuestionModel.DoesNotExist:
                pass

        score = correct
        percentage = round((score / 10) * 100, 2)

        # Save result
        QuizResult.objects.create(user=request.user, subject=subject, score=score)

        # Flag for displaying result on next GET
        request.session[f"{subject}_just_completed"] = True

        return redirect('quiz', subject=subject)

# History View
@login_required(login_url='/accounts/login/')
def quiz_history(request):
    user_results = QuizResult.objects.filter(user=request.user).order_by('-timestamp')

    summary = QuizResult.objects.filter(user=request.user).values('subject') \
        .annotate(attempts=Count('id'), avg_score=Avg('score'))

    return render(request, 'quiz/history.html', {
        'user_results': user_results,
        'summary': summary
    })

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Optional: Send email to admin
        send_mail(
            subject="Quizora Contact Form",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['youremail@example.com'],  # replace this
        )

        messages.success(request, "Thank you for contacting us!")
        return redirect('contact')

    return render(request, 'pages/contact.html')

def about_view(request):
    return render(request, 'pages/about.html')
