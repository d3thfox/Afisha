from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewListReviewAPIView.as_view()),
    path('<int:id>', views.ReviewDetailAPIView.as_view()),
]