from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('students/', views.StudentsList.as_view() ),
    path('courses/<str:pk>/', views.SurveyStudentList.as_view()),
    path('typeForm/<str:name>/', views.TypeForm_questions.as_view()),
    path('answer/<int:surveyId>/<int:questionId>/', views.Answers.as_view()),
    path('student/<str:name>/', views.ExistsStudent.as_view()),
    path('s2ip/update_database/', views.update_database),
]

urlpatterns = format_suffix_patterns(urlpatterns)
