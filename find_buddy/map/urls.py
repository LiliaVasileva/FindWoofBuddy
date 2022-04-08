from django.urls import path

from find_buddy.map.views import show_users_addresses, show_map

urlpatterns = [
    path('', show_map, name='map'),
    path('address/', show_users_addresses, name='all users map'),
]