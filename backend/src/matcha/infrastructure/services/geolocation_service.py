import os
import random
from typing import Dict, Tuple, Any


class GeolocationService:
    """
    Service de géolocalisation pour déterminer la position des utilisateurs.
    """

    def __init__(self):
        self.api_key = os.environ.get("GEOLOCATION_API_KEY", "")
        # Cache des résultats de géolocalisation pour éviter des appels répétés
        self.geo_cache: Dict[str, Dict[str, Any]] = {}

    async def get_coordinates_from_ip(self, ip_address: str) -> Tuple[float, float]:
        """
        Récupère les coordonnées géographiques (latitude, longitude) à partir d'une adresse IP.
        """
        # Vérifier dans le cache
        if ip_address in self.geo_cache:
            return (
                self.geo_cache[ip_address]["latitude"],
                self.geo_cache[ip_address]["longitude"]
            )

        # En production, appeler un service externe comme ipstack, ipapi, etc.
        # Pour le moment, simuler une position en France
        latitude = 48.8566 + random.uniform(-0.1, 0.1)  # Paris, avec une légère variation
        longitude = 2.3522 + random.uniform(-0.1, 0.1)

        # Enregistrer dans le cache
        self.geo_cache[ip_address] = {
            "latitude": latitude,
            "longitude": longitude,
            "country": "France",
            "city": "Paris"
        }

        return (latitude, longitude)

    async def get_coordinates_from_address(self, address: str) -> Tuple[float, float]:
        """
        Récupère les coordonnées géographiques à partir d'une adresse postale.
        """
        # Vérifier dans le cache
        cache_key = f"addr:{address}"
        if cache_key in self.geo_cache:
            return (
                self.geo_cache[cache_key]["latitude"],
                self.geo_cache[cache_key]["longitude"]
            )

        # En production, appeler un service comme Google Maps, Nominatim, etc.
        # Pour le moment, simuler une position
        latitude = 48.8566 + random.uniform(-0.1, 0.1)
        longitude = 2.3522 + random.uniform(-0.1, 0.1)

        # Enregistrer dans le cache
        self.geo_cache[cache_key] = {
            "latitude": latitude,
            "longitude": longitude,
            "formatted_address": address
        }

        return (latitude, longitude)

    async def calculate_distance(self, coords1: Tuple[float, float],
                                coords2: Tuple[float, float]) -> float:
        """
        Calcule la distance en kilomètres entre deux points géographiques.
        Utilise la formule de Haversine pour calculer la distance sur une sphère.
        """
        import math

        lat1, lon1 = coords1
        lat2, lon2 = coords2

        # Rayon de la Terre en kilomètres
        earth_radius = 6371.0

        # Conversion des degrés en radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Différence de longitude et latitude
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        # Formule de Haversine
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = earth_radius * c

        return distance
