"""
Views for the Lumera Cosmetics store.

Each view handles one page or action:
- home: The landing page with featured products and categories
- shop: Product listing with search, filter, and sort
- product_detail: Single product page with related products
- cart: Display the session-based shopping cart
- add_to_cart: Add a product to the cart (session-based)
- update_cart: Change the quantity of a cart item
- remove_from_cart: Remove an item from the cart
- checkout: Show the checkout form (requires login)
- place_order: Process the checkout form and create an Order
- order_confirmation: Show the order success page
- login_view: Handle user login
- register_view: Handle user registration
- logout_view: Handle user logout
- about: Static about page
- contact: Contact form page

Cart System:
The cart is stored in the user's session as a list of dicts:
    [
        {"product_id": 1, "quantity": 2},
        {"product_id": 5, "quantity": 1},
    ]
This keeps things simple and works for both logged-in and anonymous users.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Product, Category, Order, OrderItem
from .forms import RegisterForm, LoginForm, CheckoutForm, ContactForm


# ── Helper: Get cart from session ───────────────────────────
def get_cart(request):
    """Return the cart list from the session, or an empty list."""
    return request.session.get('cart', [])


def save_cart(request, cart):
    """Save the cart list back to the session."""
    request.session['cart'] = cart


def get_cart_items_and_total(request):
    """
    Given the session cart (list of {product_id, quantity}),
    look up each Product and return:
      - items: list of dicts with product object, quantity, subtotal
      - total: the grand total price
    """
    cart = get_cart(request)
    items = []
    total = 0
    for item in cart:
        product = Product.objects.filter(id=item['product_id']).first()
        if product:
            subtotal = product.price * item['quantity']
            items.append({
                'product': product,
                'quantity': item['quantity'],
                'subtotal': subtotal,
            })
            total += subtotal
    return items, total


# ── Home Page ───────────────────────────────────────────────
def home(request):
    """Landing page: hero, featured products, categories, reviews."""
    featured_products = Product.objects.filter(is_featured=True)[:8]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'categories': categories,
    })


# ── Shop / Product Listing ─────────────────────────────────
def shop(request):
    """
    Display all products with optional search, category filter,
    and price sorting. All filtering is done server-side via URL params.
    """
    products = Product.objects.all()
    categories = Category.objects.all()

    # Get filter parameters from the URL
    search_query = request.GET.get('search', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort_option = request.GET.get('sort', '').strip()

    # Filter by search query (search in name and description)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by category slug
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Sort products
    if sort_option == 'price_low':
        products = products.order_by('price')
    elif sort_option == 'price_high':
        products = products.order_by('-price')
    elif sort_option == 'rating':
        products = products.order_by('-rating')
    elif sort_option == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')

    # Determine the active category name for display
    active_category = ''
    if category_slug:
        cat = Category.objects.filter(slug=category_slug).first()
        if cat:
            active_category = cat.name

    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
        'active_category': active_category,
        'sort_option': sort_option,
    })


# ── Product Detail ──────────────────────────────────────────
def product_detail(request, slug):
    """Show a single product's details plus related products."""
    product = get_object_or_404(Product, slug=slug)
    # Related products = same category, excluding current product
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


# ── Cart Page ───────────────────────────────────────────────
def cart(request):
    """Display the shopping cart with all items and totals."""
    items, total = get_cart_items_and_total(request)
    return render(request, 'cart.html', {
        'cart_items': items,
        'total': total,
    })


# ── Add to Cart ─────────────────────────────────────────────
def add_to_cart(request, product_id):
    """
    Add a product to the session cart.
    If the product is already in the cart, increment its quantity.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    # Check if product is already in the cart
    found = False
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            found = True
            break

    # If not found, add it as a new item
    if not found:
        cart.append({'product_id': product_id, 'quantity': 1})

    save_cart(request, cart)
    messages.success(request, f'"{product.name}" added to cart!')
    # Redirect back to the page the user was on
    return redirect(request.META.get('HTTP_REFERER', 'shop'))


# ── Update Cart Quantity ────────────────────────────────────
def update_cart(request, index):
    """
    Update the quantity of a cart item at the given index.
    The quantity change (+1 or -1) is sent as a URL parameter.
    """
    cart = get_cart(request)

    if 0 <= index < len(cart):
        change = request.GET.get('change', '0')
        try:
            change = int(change)
        except ValueError:
            change = 0

        cart[index]['quantity'] += change

        # Remove the item if quantity drops to 0 or below
        if cart[index]['quantity'] <= 0:
            cart.pop(index)

    save_cart(request, cart)
    return redirect('cart')


# ── Remove from Cart ────────────────────────────────────────
def remove_from_cart(request, index):
    """Remove an item from the cart at the given index."""
    cart = get_cart(request)

    if 0 <= index < len(cart):
        removed_product = Product.objects.filter(id=cart[index]['product_id']).first()
        cart.pop(index)
        save_cart(request, cart)
        if removed_product:
            messages.info(request, f'"{removed_product.name}" removed from cart.')

    return redirect('cart')


# ── Checkout (requires login) ───────────────────────────────
@login_required
def checkout(request):
    """
    Show the checkout form with order summary.
    Pre-fills the form with the logged-in user's info if available.
    """
    items, total = get_cart_items_and_total(request)

    # Don't allow checkout with an empty cart
    if not items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the Order
            order = Order(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                pincode=form.cleaned_data['pincode'],
                total_amount=total,
            )
            order.save()

            # Create OrderItem for each cart item
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    product_price=item['product'].price,
                    quantity=item['quantity'],
                )

            # Clear the cart after successful order
            save_cart(request, [])

            return redirect('order_confirmation', order_id=order.id)
    else:
        # Pre-fill form with user data
        initial_data = {
            'full_name': request.user.first_name or '',
            'email': request.user.email or '',
        }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': items,
        'total': total,
    })


# ── Order Confirmation ──────────────────────────────────────
@login_required
def order_confirmation(request, order_id):
    """Show the order confirmation page after a successful order."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {
        'order': order,
    })


# ── Login ───────────────────────────────────────────────────
def login_view(request):
    """Handle user login using Django's authenticate() function."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or username}!')

                # Redirect to the 'next' page if set (e.g., checkout), otherwise home
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# ── Register ────────────────────────────────────────────────
def register_view(request):
    """Handle new user registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in automatically after registration
            login(request, user)
            messages.success(request, f'Welcome to Lumera, {user.first_name}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# ── Logout ──────────────────────────────────────────────────
def logout_view(request):
    """Log the user out and redirect to home."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ── About ───────────────────────────────────────────────────
def about(request):
    """Static about page."""
    return render(request, 'about.html')


# ── Contact ─────────────────────────────────────────────────
def contact(request):
    """Contact page with a simple form (no database storage)."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})