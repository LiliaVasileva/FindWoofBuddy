import folium
from geocoder import location

from find_buddy.dog.models import Dog


def def_my_map():
    dogs = Dog.objects.all()
    m = folium.Map(location=[19, -12], zoom_start=2)
    for dog in dogs:
        loc = location(dog.address)
        my_lat = loc.lat
        my_lng = loc.lng
        folium.Marker([my_lat, my_lng], tooltip="Click for woof's info",popup=f'{dog.description}').add_to(m)
    return m
