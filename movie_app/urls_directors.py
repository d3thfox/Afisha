from django.urls import path

from. import views

urlpatterns = [
    path('', views.DirectosListApiView.as_view()),
    path('<int:id>', views.DirectorDetailAPIView.as_view()),
]