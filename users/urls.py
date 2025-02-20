from django.urls import path

from . import views

urlpatterns = [
    path('registation/',views.registration_api_view),
    path('login/',views.login_api_view),
    path('confirm/' ,views.confirm_registration_api_view),
]