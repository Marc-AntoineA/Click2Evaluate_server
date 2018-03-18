from django.urls import path, include
from controlPanel import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'controlPanel'
urlpatterns = [
    path('', views.home, name = "home"),
    path('vueGlobale/', views.general, name = "generalView"),
    path('vueGlobale/<str:type_request>/', views.specific, name="specificView"),
    path('vueQuestions/', views.question_home, name="questionViewHome"),
    path('vueQuestions/<int:id_q>/', views.question, name="questionView"),
    path('import/', views.importDb, name = "importDb"),
    path('export/', views.exportDb, name = "exportDb"),
    path('projet/', views.project, name = "project"),
    path('questionnaires/', views.typeFormView, name = "typeForm"),
    path('questionnaires/<int:id_q>/', views.typeFormView, name="typeFormSpecific"),
    path('questionnaires/edit/<int:id_q>/', views.typeFormEditView, name="typeFormEdit"),
    path('questionnaires/edit/', views.typeFormEditView, name="typeFormEditGeneral"),
    path('connecter/', views.connect, name = "connect"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
