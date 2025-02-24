from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieViewAPIView.as_view()),
    path('<int:id>', views.MovieDetailAPIView.as_view()),
    path('reviews/', views.MovieListReviewsApiView.as_view()),
]