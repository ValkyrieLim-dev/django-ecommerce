from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Order, OrderItem

# --- Cart session key ---
CART_SESSION_ID = 'cart'

# --- Helper: get cart from session ---
def _get_cart(request):
    return request.session.setdefault(CART_SESSION_ID, {})

# --- Home / root ---
def home(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
    return redirect('store:login')

# --- User Login ---
def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')  # Already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('store:product_list')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'store/login.html')

# --- User Register ---
def register(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return render(request, 'store/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'store/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Account created and logged in!")
            return redirect('store:product_list')

    return render(request, 'store/register.html')

# --- Product List ---
@login_required(login_url='store:login')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# --- Product Detail ---
@login_required(login_url='store:login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# --- Add to Cart ---
@login_required(login_url='store:login')
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1))
    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += qty
    else:
        cart[str(product.id)] = {'quantity': qty, 'price': str(product.price)}
    request.session.modified = True
    return redirect('store:cart_detail')

# --- Remove from Cart ---
@login_required(login_url='store:login')
def cart_remove(request, pk):
    cart = _get_cart(request)
    if str(pk) in cart:
        del cart[str(pk)]
        request.session.modified = True
    return redirect('store:cart_detail')

# --- View Cart ---
@login_required(login_url='store:login')
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
@login_required(login_url='store:login')
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('store:product_list')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        order = Order.objects.create(name=name, email=email, address=address)

        for pid, item in cart.items():
            p = Product.objects.get(pk=int(pid))
            qty = int(item.get('quantity', 0))
            OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
            p.stock = max(0, p.stock - qty)
            p.save()

        request.session[CART_SESSION_ID] = {}
        request.session.modified = True
        return redirect(reverse('store:checkout_success', args=[order.id]))

    total = 0
    products = Product.objects.filter(id__in=cart.keys())
    for p in products:
        item = cart[str(p.id)]
        total += int(item.get('quantity', 0)) * float(item.get('price', p.price))

    return render(request, 'store/checkout.html', {'total': total})

# --- Checkout Success ---
@login_required(login_url='store:login')
def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/checkout_success.html', {'order': order})
