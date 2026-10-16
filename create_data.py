import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_amazon.settings')
django.setup()

from store.models import Category, Product

print("Before:", Category.objects.count(), Product.objects.count())

# Categories already irukku, so first category eduthukalam
c1 = Category.objects.first()

if c1:
    Product.objects.all().delete() # Pazhasa delete pannidalam
    Product.objects.create(name="Headphone", price=1999, category=c1, description="Good quality", image="products/images_1.jpg")
    Product.objects.create(name="Smart Watch", price=2999, category=c1, description="Smart watch", image="products/images_2.jpg")
    Product.objects.create(name="T-Shirt", price=499, category=c1, description="Cotton", image="products/images_3.jpg")
    print("Products Created!")

print("After:", Category.objects.count(), Product.objects.count())