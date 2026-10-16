from django.db import migrations


def add_electronics_products(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    Product = apps.get_model("store", "Product")
    database = schema_editor.connection.alias

    electronics, _ = Category.objects.using(database).get_or_create(
        name="Electronics"
    )
    products = (
        (
            "Bluetooth Headphones",
            "2499.00",
            "products/images_7.jpg",
            "Wireless over-ear headphones with comfortable ear cushions.",
        ),
        (
            "Gaming Keyboard",
            "3499.00",
            "products/images_6.jpg",
            "Colorful mechanical keyboard for gaming and everyday typing.",
        ),
    )
    for name, price, image, description in products:
        Product.objects.using(database).get_or_create(
            name=name,
            category=electronics,
            defaults={
                "price": price,
                "image": image,
                "description": description,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_add_fashion_and_gadgets"),
    ]

    operations = [
        migrations.RunPython(add_electronics_products, migrations.RunPython.noop),
    ]
