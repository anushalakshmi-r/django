from django.test import TestCase
from django.test import override_settings

from .models import Category


class HomeCatalogTests(TestCase):
    def test_home_displays_products_in_each_category_with_descriptions(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Electronics")
        self.assertContains(response, "Fashion")
        self.assertContains(response, "Gadgets")
        self.assertContains(response, "Jeans")
        self.assertContains(response, "Classic blue denim jeans")
        self.assertContains(response, "T-Shirt")
        self.assertContains(response, "Comfortable everyday cotton T-shirt")
        self.assertContains(response, "Mechanical Keyboard")
        self.assertContains(response, "Responsive mechanical keyboard")
        self.assertContains(response, "Wireless Headphones")
        self.assertContains(response, "Comfortable wireless headphones")
        self.assertContains(response, "/media/products/images_4.jpg")
        self.assertContains(response, "/media/products/images_5.jpg")
        self.assertContains(response, "/media/products/images_6.jpg")
        self.assertContains(response, "/media/products/images_7.jpg")

        fashion = Category.objects.get(name="Fashion")
        gadgets = Category.objects.get(name="Gadgets")
        self.assertSetEqual(
            set(fashion.products.values_list("name", flat=True)),
            {"Jeans", "T-Shirt"},
        )
        self.assertSetEqual(
            set(gadgets.products.values_list("name", flat=True)),
            {"Mechanical Keyboard", "Wireless Headphones"},
        )

    @override_settings(
        DEBUG=False,
        ALLOWED_HOSTS=["testserver"],
        SECURE_SSL_REDIRECT=False,
    )
    def test_product_images_are_served_when_debug_is_disabled(self):
        response = self.client.get("/media/products/images_4.jpg")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/jpeg")
