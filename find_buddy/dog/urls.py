from django.urls import path

from find_buddy.dog.views import DogsTemplateView, DogCreateView, DogEditView, dog_delete_view, DogDetailsView, \
    dog_missing_report

urlpatterns = [
    path('details/', DogsTemplateView.as_view(), name='owner dogs'),
    path('create/', DogCreateView.as_view(), name='dog create'),
    path('edit/<int:pk>', DogEditView.as_view(), name='dog edit'),
    path('delete/<int:pk>', dog_delete_view, name='dog delete'),
    path('details/<int:pk>', DogDetailsView.as_view(), name ='dog detail page'),
    path('missing/', dog_missing_report, name='dog missing report'),
    ]