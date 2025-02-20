from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list_create_api_view),
    path('<int:id>', views.movie_detail_update_api_view),
    path('reviews/', views.movie_list_review_api_view)
]