"""Simple geocoding module to convert place names to latitude/longitude coordinates."""

import httpx

async def geocode(place_name):
    """
    Convert a place name to latitude/longitude coordinates using Nominatim API.
    
    Args:
        place_name: String with the place name to geocode
        
    Returns:
        tuple: (latitude, longitude) if successful, (None, None) if failed
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1,
    }
    
    headers = {
        "User-Agent": "WeatherMCP/1.0",
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return (lat, lon)
            else:
                return (None, None)
    except Exception as e:
        print(f"Geocoding error: {e}")
        return (None, None)
