from django.contrib import admin
from django.urls import path,include
from Home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('quiz/<str:subject>/rules/', rules_page, name='rules_page'),
    path('quiz/<str:subject>/start/', start_quiz, name='start_quiz'),
    path('quiz/<str:subject>/', quiz_view, name='quiz'),
    path('accounts/', include('accounts.urls')),
    path('history/', quiz_history, name='quiz_history'),
]
