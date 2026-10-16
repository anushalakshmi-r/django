from django.db import migrations


def seed_catalog(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    Product = apps.get_model("store", "Product")

    categories = {}
    for name in ("Electronics", "Fashion", "Gadgets"):
        categories[name], _ = (
            Category.objects.using(schema_editor.connection.alias).get_or_create(
                name=name
            )
        )

    products = (
        ("Headphone", "1999.00", "products/images_1.jpg", "Good quality"),
        ("Smart Watch", "2999.00", "products/images_2.jpg", "Smart watch"),
        ("T-Shirt", "499.00", "products/images_3.jpg", "Cotton"),
    )
    for name, price, image, description in products:
        Product.objects.using(schema_editor.connection.alias).get_or_create(
            name=name,
            category=categories["Electronics"],
            defaults={
                "price": price,
                "image": image,
                "description": description,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_order_orderitem"),
    ]

    operations = [
        migrations.RunPython(seed_catalog, migrations.RunPython.noop),
    ]
