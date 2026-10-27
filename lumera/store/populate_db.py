"""
Management command to populate the database with sample categories and products.

Run this command AFTER migrations:
    python manage.py populate_db

It creates 6 categories and 18 products (3 per category).
If a category or product with the same name/slug already exists,
it will be skipped to avoid duplicates on repeated runs.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from lumera.store.models import Category, Product


class Command(BaseCommand):
    help = 'Populate the database with sample Lumera Cosmetics categories and products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating database with sample data...\n'))

        # ── Categories ──────────────────────────────────────
        categories_data = [
            {
                'name': 'Skincare',
                'description': 'Nourish and protect your skin with our curated skincare collection.'
            },
            {
                'name': 'Makeup',
                'description': 'Enhance your natural beauty with our premium makeup essentials.'
            },
            {
                'name': 'Lip Care',
                'description': 'Keep your lips soft, smooth, and beautifully colored.'
            },
            {
                'name': 'Hair Care',
                'description': 'Transform your hair with our nourishing hair care range.'
            },
            {
                'name': 'Body Care',
                'description': 'Pamper your body with luxurious lotions, washes, and scrubs.'
            },
            {
                'name': 'Fragrance',
                'description': 'Discover your signature scent from our exquisite fragrance line.'
            },
        ]

        created_categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                }
            )
            created_categories[cat.name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created category: {cat.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Category already exists: {cat.name}'))

        # ── Products ────────────────────────────────────────
        products_data = [
            # Skincare
            {
                'name': 'Rose Glow Hydrating Serum',
                'category': 'Skincare',
                'price': 34.99,
                'rating': 4.8,
                'description': 'A lightweight, fast-absorbing serum infused with rose extract and hyaluronic acid to deeply hydrate and illuminate your skin. Perfect for all skin types, this serum leaves your complexion dewy and radiant.',
                'featured': True,
            },
            {
                'name': 'Vitamin C Brightening Moisturizer',
                'category': 'Skincare',
                'price': 28.99,
                'rating': 4.6,
                'description': 'Enriched with stabilized vitamin C and niacinamide, this daily moisturizer brightens uneven skin tone and provides all-day hydration without feeling heavy or greasy.',
                'featured': False,
            },
            {
                'name': 'Gentle Renewal Exfoliating Toner',
                'category': 'Skincare',
                'price': 22.99,
                'rating': 4.5,
                'description': 'Formulated with AHA and BHA, this gentle toner removes dead skin cells, refines pores, and reveals a fresh, radiant complexion without irritation.',
                'featured': False,
            },
            # Makeup
            {
                'name': 'Silk Finish Foundation',
                'category': 'Makeup',
                'price': 38.99,
                'rating': 4.7,
                'description': 'A buildable, medium-coverage foundation with a silky-smooth finish that blurs imperfections and lasts up to 24 hours. Available in 20 shades for every skin tone.',
                'featured': True,
            },
            {
                'name': 'Warm Blush Palette',
                'category': 'Makeup',
                'price': 32.99,
                'rating': 4.4,
                'description': 'Six blendable shades from soft peach to deep berry, perfect for creating a natural flush or a bold sculpted look. Ultra-pigmented and long-wearing.',
                'featured': False,
            },
            {
                'name': 'Lengthening Mascara',
                'category': 'Makeup',
                'price': 24.99,
                'rating': 4.6,
                'description': 'A clump-free, smudge-proof formula that adds dramatic length and volume to every lash for a wide-awake look that lasts all day.',
                'featured': False,
            },
            # Lip Care
            {
                'name': 'Velvet Matte Lipstick - Crimson Rose',
                'category': 'Lip Care',
                'price': 19.99,
                'rating': 4.8,
                'description': 'A richly pigmented, long-wearing matte lipstick that glides on smoothly and delivers bold, velvety color that lasts all day without drying your lips.',
                'featured': True,
            },
            {
                'name': 'Hydrating Lip Gloss - Peach Glow',
                'category': 'Lip Care',
                'price': 16.99,
                'rating': 4.3,
                'description': 'A non-sticky, high-shine gloss infused with vitamin E and jojoba oil to keep lips soft, plump, and luminous with a sheer wash of peachy color.',
                'featured': False,
            },
            {
                'name': 'Overnight Lip Treatment',
                'category': 'Lip Care',
                'price': 21.99,
                'rating': 4.7,
                'description': 'A deeply nourishing overnight treatment with shea butter and chamomile that repairs and revitalizes dry, cracked lips while you sleep. Wake up to baby-soft lips.',
                'featured': False,
            },
            # Hair Care
            {
                'name': 'Argan Oil Repair Shampoo',
                'category': 'Hair Care',
                'price': 26.99,
                'rating': 4.5,
                'description': 'A sulfate-free, gentle cleansing formula enriched with cold-pressed argan oil to restore moisture, shine, and strength to damaged, color-treated hair.',
                'featured': True,
            },
            {
                'name': 'Keratin Deep Conditioner',
                'category': 'Hair Care',
                'price': 29.99,
                'rating': 4.6,
                'description': 'An intensive conditioning treatment packed with keratin protein and coconut oil to smooth frizz, repair breakage, and improve elasticity for salon-smooth hair.',
                'featured': False,
            },
            {
                'name': 'Shine Boost Hair Serum',
                'category': 'Hair Care',
                'price': 23.99,
                'rating': 4.4,
                'description': 'A lightweight, non-greasy serum that adds instant shine, tames flyaways, and protects hair from heat damage up to 450 degrees Fahrenheit.',
                'featured': False,
            },
            # Body Care
            {
                'name': 'Shea Butter Body Lotion',
                'category': 'Body Care',
                'price': 24.99,
                'rating': 4.7,
                'description': 'A rich, creamy lotion infused with raw shea butter and oat extract to deeply nourish and soften dry skin from head to toe. Absorbs quickly with no greasy residue.',
                'featured': True,
            },
            {
                'name': 'Coconut Milk Body Wash',
                'category': 'Body Care',
                'price': 18.99,
                'rating': 4.5,
                'description': 'A gentle, creamy body wash with real coconut milk and aloe vera that cleanses without stripping natural moisture. Leaves skin feeling soft and lightly fragranced.',
                'featured': False,
            },
            {
                'name': 'Exfoliating Body Scrub',
                'category': 'Body Care',
                'price': 27.99,
                'rating': 4.6,
                'description': 'A luxurious sugar scrub blended with essential oils and vitamin E to smooth, polish, and revitalize dull, rough skin. Reveals silky-soft, glowing skin.',
                'featured': False,
            },
            # Fragrance
            {
                'name': 'Midnight Rose Eau de Parfum',
                'category': 'Fragrance',
                'price': 64.99,
                'rating': 4.9,
                'description': 'An enchanting fragrance opening with bergamot and pink pepper, blooming into a heart of Turkish rose, and settling into warm oud and amber. 50ml spray bottle.',
                'featured': True,
            },
            {
                'name': 'Fresh Bloom Body Mist',
                'category': 'Fragrance',
                'price': 28.99,
                'rating': 4.4,
                'description': 'A light, refreshing mist with notes of white jasmine, peony, and fresh linen. Perfect for an everyday delicate scent. 200ml bottle.',
                'featured': False,
            },
            {
                'name': 'Warm Vanilla Perfume Oil',
                'category': 'Fragrance',
                'price': 22.99,
                'rating': 4.6,
                'description': 'A roll-on perfume oil with warm vanilla bean, sandalwood, and a touch of caramel for a cozy, long-lasting intimate scent. Perfect for travel. 10ml roller.',
                'featured': False,
            },
        ]

        for prod_data in products_data:
            category = created_categories[prod_data['category']]
            product, created = Product.objects.get_or_create(
                slug=slugify(prod_data['name']),
                defaults={
                    'name': prod_data['name'],
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'rating': prod_data['rating'],
                    'stock': 15,
                    'is_featured': prod_data['featured'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Product already exists: {product.name}'))

        self.stdout.write(self.style.SUCCESS('\nDatabase population complete!'))