from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
import os

class MapViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_map_view_loads(self):
        """Test that the map page loads successfully"""
        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Leaflet', response.content.decode())

    def test_static_files_served(self):
        """Test that static files exist on disk"""
        map_js = os.path.join(settings.BASE_DIR, 'static', 'js', 'map.js')
        styles_css = os.path.join(settings.BASE_DIR, 'static', 'css', 'styles.css')

        self.assertTrue(os.path.exists(map_js), f"map.js not found at {map_js}")
        self.assertTrue(os.path.exists(styles_css), f"styles.css not found at {styles_css}")
