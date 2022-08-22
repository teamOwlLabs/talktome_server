from django.urls import path

from doorbell import views

urlpatterns = [
    path('visit/', views.VisitView().as_view()),
    path('category/', views.CategoryListCreateView().as_view()),
    path('token/', views.FCMTokenCreateView().as_view()),
]