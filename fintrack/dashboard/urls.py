from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('budget/', views.budget, name='budget'),
    path('expenseprediction/', views.expenseprediction, name='budget'),
    path('generatereport/', views.generatereport, name='generatereport'),
    path('analysis/', views.analysis, name='analysis'),
    path('addCategoriesData/', views.form_view, name='formdata'),
    path('limitdata/', views.limitdata, name='limitdata'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('expense/prediction', views.predict_expense, name='predict_expense'),
    path('analysis/showanalysis', views.showanalysis, name='showanalysis'), 
    path('generatereport/<str:period>/', views.export_report, name='export_report'),
    path('budget/limitGraph', views.limitGraph, name='limitGraph'),
]
