from django.urls import path, include
from controlPanel import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'controlPanel'
urlpatterns = [
    path('accueil/', views.home, name = "home"),
    path('vueGlobale/', views.general, name = "generalView"),
    path('import/', views.importDb, name = "importDb"),
    path('export/', views.exportDb, name = "exportDb"),
    path('projet', views.project, name = "project"),
    path('questionnaires/', views.survey, name = "survey"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
