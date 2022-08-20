from django.urls import path

from doorbell import views

urlpatterns = [
    path('visit/', views.VisitView().as_view()),
]