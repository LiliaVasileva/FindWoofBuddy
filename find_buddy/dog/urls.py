from django.urls import path

from find_buddy.dog.views import DogsTemplateView, DogCreateView, DogEditView, dog_delete_view

urlpatterns = [
    path('details/', DogsTemplateView.as_view(), name='dog details'),
    path('create/', DogCreateView.as_view(), name='dog create'),
    path('edit/<int:pk>', DogEditView.as_view(), name='dog edit'),
    path('delete/<int:pk>', dog_delete_view, name='dog delete'),
    ]