from django.shortcuts import render, redirect
import folium
import geocoder
from geocoder import location
from .forms import SearchForm
from find_buddy.map.models import Search
from ..common.helpers import def_my_map


def show_map(request):
    nav_bar = True
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('map')

    else:
        form = SearchForm()
    address = Search.objects.all().last()
    loc = location(str(address))
    my_lat = loc.lat
    my_lng = loc.lng

    if not request.user.pk:
        nav_bar = False
        return redirect('page 404')

    if my_lat is None or my_lng is None:
        address.delete()
        nav_bar = False
        return redirect('page 404')
    # Create MAP Object
    m = folium.Map(location=[19, -12], zoom_start=2)
    folium.Marker([my_lat, my_lng], tooltip='You have a friend near by', popup='I will decide later',
                  draggable=True).add_to(m)
    m = m._repr_html_()  # we need to create a html representation of the map object
    context = {
        'map': m,
        'form': form,
        'nav_bar': nav_bar,
    }
    return render(request, 'home-map.html', context)


def show_users_addresses(request):
    my_map = def_my_map()
    context = {
        'my_map': my_map
    }
    return render(request, 'users-map.html', context)
