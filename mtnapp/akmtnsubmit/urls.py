from django.urls import path
from akmtnsubmit import views

urlpatterns = [
    path("", views.home, name="home"),
    path('submit/', views.SubmitView.as_view(), name='submit'),
    path('scores/', views.ScoresView.as_view(), name='scores'),

]