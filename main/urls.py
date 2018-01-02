from django.urls import path, include
from main import views
from rest_framework.urlpatterns import format_suffix_patterns
from main import views


urlpatterns = [
    path('students/', views.StudentsList.as_view() ),
    path('courses/<str:pk>/', views.AnswersStudentList.as_view()),
    path('typeForm/<str:name>/', views.TypeFormDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
