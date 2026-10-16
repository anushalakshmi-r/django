from django.db import migrations


def add_category_products(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    Product = apps.get_model("store", "Product")
    database = schema_editor.connection.alias

    fashion, _ = Category.objects.using(database).get_or_create(name="Fashion")
    gadgets, _ = Category.objects.using(database).get_or_create(name="Gadgets")

    shirt = (
        Product.objects.using(database)
        .filter(name__iexact="T-Shirt")
        .order_by("pk")
        .first()
    )
    if shirt is None:
        shirt = Product(name="T-Shirt")
    shirt.category = fashion
    shirt.price = "499.00"
    shirt.image = "products/images_5.jpg"
    shirt.description = "Comfortable everyday cotton T-shirt."
    shirt.save(using=database)

    fashion_products = (
        (
            "Jeans",
            "1299.00",
            "products/images_4.jpg",
            "Classic blue denim jeans for everyday wear.",
        ),
    )
    for name, price, image, description in fashion_products:
        Product.objects.using(database).get_or_create(
            name=name,
            category=fashion,
            defaults={
                "price": price,
                "image": image,
                "description": description,
            },
        )

    gadget_products = (
        (
            "Mechanical Keyboard",
            "2999.00",
            "products/images_6.jpg",
            "Responsive mechanical keyboard for work and gaming.",
        ),
        (
            "Wireless Headphones",
            "1999.00",
            "products/images_7.jpg",
            "Comfortable wireless headphones for music and calls.",
        ),
    )
    for name, price, image, description in gadget_products:
        Product.objects.using(database).get_or_create(
            name=name,
            category=gadgets,
            defaults={
                "price": price,
                "image": image,
                "description": description,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_seed_catalog"),
    ]

    operations = [
        migrations.RunPython(add_category_products, migrations.RunPython.noop),
    ]
