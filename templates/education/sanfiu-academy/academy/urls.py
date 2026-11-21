from django.urls import path
from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("learn/", views.dashboard, name="dashboard"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("courses/<slug:slug>/enroll/", views.enroll, name="enroll"),
    path("courses/<slug:course_slug>/lessons/<slug:lesson_slug>/", views.lesson_detail, name="lesson_detail"),
    path("courses/<slug:course_slug>/lessons/<slug:lesson_slug>/complete/", views.complete_lesson, name="complete_lesson"),
]
