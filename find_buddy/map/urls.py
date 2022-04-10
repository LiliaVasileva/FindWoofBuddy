from django.urls import path

from find_buddy.map.views import show_map

urlpatterns = [
    path('', show_map, name='map'),
]