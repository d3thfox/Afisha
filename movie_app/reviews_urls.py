from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list_api_create_view),
    path('<int:id>', views.review_detail_update_api_view),
]