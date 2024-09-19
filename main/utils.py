# main/utils.py

import requests
from django.conf import settings


def get_location_name(lat, lng):
    """Fetch the location name using Google Geocoding API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={settings.GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data['results']:
        # Return the first formatted address
        return data['results'][0]['formatted_address']
    return "Location Not Available"


def get_route_url(start_lat, start_lng, end_lat, end_lng):
    """Return the Google Maps route URL from start to end location."""
    return f"https://www.google.com/maps/dir/?api=1&origin={start_lat},{start_lng}&destination={end_lat},{end_lng}"
