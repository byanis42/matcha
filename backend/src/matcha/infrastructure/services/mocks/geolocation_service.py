from typing import Dict, Tuple, Any
import math


class MockGeolocationService:
    """
    Version simulée du service de géolocalisation pour les tests.
    """

    def __init__(self):
        # Cache simulé contenant des positions prédéfinies
        self.geo_cache: Dict[str, Dict[str, Any]] = {
            "127.0.0.1": {"latitude": 48.8566, "longitude": 2.3522, "country": "France", "city": "Paris"},
            "192.168.1.1": {"latitude": 51.5074, "longitude": -0.1278, "country": "UK", "city": "London"},
            "10.0.0.1": {"latitude": 40.7128, "longitude": -74.0060, "country": "USA", "city": "New York"},
        }

        # Correspondances adresses -> coordonnées
        self.address_mapping: Dict[str, Dict[str, Any]] = {
            "addr:Paris, France": {"latitude": 48.8566, "longitude": 2.3522, "formatted_address": "Paris, France"},
            "addr:London, UK": {"latitude": 51.5074, "longitude": -0.1278, "formatted_address": "London, UK"},
            "addr:New York, USA": {"latitude": 40.7128, "longitude": -74.0060, "formatted_address": "New York, USA"},
        }

    async def get_coordinates_from_ip(self, ip_address: str) -> Tuple[float, float]:
        """
        Récupère des coordonnées simulées pour une adresse IP.
        """
        if ip_address in self.geo_cache:
            return (
                self.geo_cache[ip_address]["latitude"],
                self.geo_cache[ip_address]["longitude"]
            )

        # Valeur par défaut si l'IP n'est pas connue
        return (48.8566, 2.3522)

    async def get_coordinates_from_address(self, address: str) -> Tuple[float, float]:
        """
        Récupère des coordonnées simulées pour une adresse postale.
        """
        cache_key = f"addr:{address}"
        if cache_key in self.address_mapping:
            return (
                self.address_mapping[cache_key]["latitude"],
                self.address_mapping[cache_key]["longitude"]
            )

        # Valeur par défaut si l'adresse n'est pas connue
        return (48.8566, 2.3522)

    async def calculate_distance(self, coords1: Tuple[float, float],
                                coords2: Tuple[float, float]) -> float:
        """
        Calcule la distance en kilomètres entre deux points simulés.
        Utilise la formule de Haversine comme la version réelle.
        """
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

    def add_test_location(self, identifier: str, latitude: float, longitude: float,
                         city: str = "Test City", country: str = "Test Country"):
        """
        Ajoute une position de test au cache.
        """
        if identifier.startswith("addr:"):
            self.address_mapping[identifier] = {
                "latitude": latitude,
                "longitude": longitude,
                "formatted_address": identifier[5:]
            }
        else:
            self.geo_cache[identifier] = {
                "latitude": latitude,
                "longitude": longitude,
                "country": country,
                "city": city
            }
