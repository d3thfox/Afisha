from django.urls import path

from . import views

urlpatterns = [
    path('registation/',views.RegisterAPIView.as_view()),
    path('login/',views.LoginAPIView.as_view()),
    path('confirm/' ,views.ConfirmRegisterAPIView.as_view()),
]