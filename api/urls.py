from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as viewsAuth

urlpatterns = [
    #path('students/', views.StudentsList.as_view()),
    path('courses/<str:pk>/', views.SurveyStudentList.as_view()), #areCoursesFromStudent
    path('typeForm/<str:name>/', views.TypeForm_questions.as_view()),  # isAuthenticated
    path('answer/<int:surveyId>/<int:questionId>/', views.Answers.as_view()), #isAnswerFromStudent
    #path('student/<str:name>/', views.ExistsStudent.as_view()),
    path('connect/', viewsAuth.obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
