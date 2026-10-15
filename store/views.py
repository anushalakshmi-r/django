
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.views.decorators.http import require_POST


def home(request):
    categories = Category.objects.all()
    products = Product.objects.select_related("category").all()

    return render(request, "store/home.html", {
        "categories": categories,
        "products": products,
    })


from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    products = Product.objects.select_related("category").all()

    return render(request, "store/home.html", {
        "categories": categories,
        "products": products,
    })


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        id=product_id
    )

    return render(request, "store/product_detail.html", {
        "product": product,
        "cart_count": sum(request.session.get("cart", {}).values()),
    })

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})
    key = str(product.id)

    cart[key] = cart.get(key, 0) + 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0
    cleaned_cart = {}

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()

        if product and quantity > 0:
            subtotal = product.price * quantity
            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })
            total += subtotal
            cleaned_cart[str(product.id)] = quantity

    if cleaned_cart != cart:
        request.session["cart"] = cleaned_cart

    return render(request, "store/cart.html", {
        "items": items,
        "total": total,
        "cart_count": sum(cleaned_cart.values()),
    })


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


@require_POST
def update_cart(request, product_id):
    cart = request.session.get("cart", {})
    key = str(product_id)

    if key in cart:
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity <= 0:
            cart.pop(key, None)
        else:
            cart[key] = min(quantity, 99)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category, Order, OrderItem


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = int(quantity)

        if quantity < 1:
            continue

        subtotal = product.price * quantity
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })
        total += subtotal

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        payment_method = request.POST.get("payment_method", "COD")

        if not customer_name or not phone or not address:
            messages.error(request, "Please fill in all delivery details.")
        elif not phone.isdigit() or not 10 <= len(phone) <= 15:
            messages.error(request, "Enter a valid phone number.")
        elif payment_method not in ["COD", "ONLINE"]:
            messages.error(request, "Choose a valid payment method.")
        else:
            order = Order.objects.create(
                customer_name=customer_name,
                phone=phone,
                address=address,
                payment_method=payment_method,
                order_status="PENDING" if payment_method == "ONLINE" else "CONFIRMED",
                total_amount=total,
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price,
                )

            if payment_method == "ONLINE":
                request.session["pending_order_id"] = order.id
                return redirect("payment")

            request.session["last_order_id"] = order.id
            request.session["cart"] = {}
            request.session.modified = True
            return redirect("order_success", order_id=order.id)

    return render(request, "store/checkout.html", {
        "items": items,
        "total": total,
        "cart_count": sum(int(q) for q in cart.values()),
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.session.get("last_order_id") != order.id:
        messages.error(request, "Please place an order first.")
        return redirect("home")

    return render(request, "store/order_success.html", {
        "order": order,
    })



def payment(request):
    order_id = request.session.get("pending_order_id")

    if not order_id:
        messages.error(request, "No pending order found.")
        return redirect("cart")

    order = get_object_or_404(
        Order,
        id=order_id,
        payment_method="ONLINE",
        order_status="PENDING"
    )

    if request.method == "POST":
        action = request.POST.get("payment_action")

        if action == "success":
            order.order_status = "CONFIRMED"
            order.save(update_fields=["order_status"])

            request.session["last_order_id"] = order.id
            request.session.pop("pending_order_id", None)
            request.session["cart"] = {}
            request.session.modified = True

            return redirect("order_success", order_id=order.id)

        elif action == "failure":
            messages.error(
                request,
                "Payment failed! Your cart is safe. Please try again."
            )
            # Important: Do not clear the cart or pending order here.

    return render(request, "store/payment.html", {
        "order": order,
    })
