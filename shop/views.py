from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Pizza, Order


def index(request):
    return render(request, 'shop/index.html')


def menu(request):
    pizzas = Pizza.objects.all()
    return render(request, 'shop/menu.html', {'pizzas': pizzas})


def order_pizza(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)

    if request.method == 'POST':
        size = request.POST['size']
        quantity = int(request.POST['quantity'])
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']

        # Calculate price based on size
        if size == "Small":
            price = pizza.small_price
        elif size == "Medium":
            price = pizza.medium_price
        else:
            price = pizza.large_price

        total = price * quantity

        Order.objects.create(
            pizza=pizza,
            size=size,
            quantity=quantity,
            customer_name=name,
            phone=phone,
            address=address,
            total_price=total
        )

        # ✅ Email inside POST
        message = f"""
New Order Received 🍕

Customer Name: {name}
Phone: {phone}
Address: {address}

Pizza: {pizza.name}
Size: {size}
Quantity: {quantity}
Total Price: ₹{total}
"""

        send_mail(
            subject="New Pizza Order 🍕",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return redirect('menu')   # ✅ only after POST

    # 👇 This must be outside POST
    return render(request, 'shop/order.html', {'pizza': pizza})


def contact(request):
    return render(request, 'shop/contact.html')