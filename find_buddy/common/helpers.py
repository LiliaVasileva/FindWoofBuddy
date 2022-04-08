import folium
from geocoder import location

from find_buddy.home.models import Profile
from find_buddy.map.models import Search


def def_my_map():
    m = folium.Map(location=[19, -12], zoom_start=2)
    for obj in Search.objects.all():
        loc = location(str(obj))
        my_lat = loc.lat
        my_lng = loc.lng
        folium.Marker([my_lat, my_lng], tooltip='You have a friend near by').add_to(m)
    m = m._repr_html_()

    return m
