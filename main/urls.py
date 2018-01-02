from django.urls import path, include
from main import views
from rest_framework.urlpatterns import format_suffix_patterns
from main import views


urlpatterns = [
    path('api/students/', views.StudentsList.as_view() ),
    path('api/courses/<str:pk>/', views.SurveyStudentList.as_view()),
    path('api/typeForm/<str:name>/', views.TypeForm.as_view()),
    path('api/answer/<int:surveyId>/<int:questionId>/', views.Answers.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
