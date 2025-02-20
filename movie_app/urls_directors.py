from django.urls import path

from. import views

urlpatterns = [
    path('', views.directors_list_create_api_view),
    path('<int:id>', views.directors_detail_update_api_view),
]