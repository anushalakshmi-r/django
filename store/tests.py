from django.test import TestCase


class HomeCatalogTests(TestCase):
    def test_home_displays_seeded_categories_and_products(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Electronics")
        self.assertContains(response, "Fashion")
        self.assertContains(response, "Gadgets")
        self.assertContains(response, "Headphone")
        self.assertContains(response, "Smart Watch")
        self.assertContains(response, "T-Shirt")
