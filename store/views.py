from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from .models import Product, Order, OrderItem

# --- Cart session key ---
CART_SESSION_ID = 'cart'

# --- Helper: get cart from session ---
def _get_cart(request):
    """
    Returns the cart dictionary stored in the session.
    If it doesn't exist, creates an empty cart.
    """
    return request.session.setdefault(CART_SESSION_ID, {})

# --- Product List ---
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# --- Product Detail ---
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# --- Add to Cart ---
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1))
    item = cart.get(str(product.id), {'quantity': 0})
    item['quantity'] += qty
    item['price'] = str(product.price)
    cart[str(product.id)] = item
    request.session.modified = True
    return redirect('store:cart_detail')

# --- Remove from Cart ---
def cart_remove(request, pk):
    cart = _get_cart(request)
    cart.pop(str(pk), None)
    request.session.modified = True
    return redirect('store:cart_detail')

# --- View Cart ---
def cart_detail(request):
    cart = _get_cart(request)
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0
    for p in products:
        item = cart[str(p.id)]
        qty = item.get('quantity', 0)
        price = float(item.get('price', p.price))
        subtotal = qty * price
        total += subtotal
        cart_items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

# --- Checkout ---
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('store:product_list')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email','')
        address = request.POST.get('address','')
        order = Order.objects.create(name=name, email=email, address=address)
        
        for pid, item in cart.items():
            p = Product.objects.get(pk=int(pid))
            qty = int(item.get('quantity',0))
            OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
            # reduce stock
            p.stock = max(0, p.stock - qty)
            p.save()

        # clear cart
        request.session[CART_SESSION_ID] = {}
        request.session.modified = True
        return redirect(reverse('store:checkout_success', args=[order.id]))

    # GET -> show checkout form
    total = 0
    products = Product.objects.filter(id__in=cart.keys())
    for p in products:
        item = cart[str(p.id)]
        total += int(item.get('quantity',0)) * float(item.get('price',p.price))
    
    return render(request, 'store/checkout.html', {'total': total})

# --- Checkout Success ---
def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/checkout_success.html', {'order': order})
import random

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # --- People also viewed: 3 random other products ---
    other_products = Product.objects.exclude(pk=pk)
    recommended = random.sample(list(other_products), min(len(other_products), 3))

    return render(request, 'store/product_detail.html', {
        'product': product,
        'recommended': recommended
    })
def cart_add(request, pk):
    """
    Add a product to the cart (or update quantity if already exists).
    """
    product = get_object_or_404(Product, pk=pk)
    cart = _get_cart(request)
    
    # Get quantity from POST (default 1)
    qty = int(request.POST.get('quantity', 1))
    
    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += qty
    else:
        cart[str(product.id)] = {'quantity': qty, 'price': str(product.price)}

    request.session.modified = True
    return redirect('store:cart_detail')
def cart_detail(request):
    cart = _get_cart(request)
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0
    for p in products:
        item = cart[str(p.id)]
        qty = item.get('quantity', 0)
        price = float(item.get('price', p.price))
        subtotal = qty * price
        total += subtotal
        cart_items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})
def cart_remove(request, pk):
    cart = _get_cart(request)
    if str(pk) in cart:
        del cart[str(pk)]
        request.session.modified = True
    return redirect('store:cart_detail')
