import os
import django
import random
import urllib.parse
import urllib.request
import json
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyshop.settings')
django.setup()

from products.models import Product

CATEGORIES = {
    'vegetables-fruits': [
        ('Organic Bananas', 1.99, 'Banana'), ('Red Apples', 2.49, 'Apple'), ('Fresh Strawberries', 3.99, 'Strawberry'),
        ('Baby Spinach', 2.99, 'Spinach'), ('Hass Avocados', 4.50, 'Avocado'), 
        ('Carrots', 1.20, 'Carrot'), ('Broccoli Crowns', 2.10, 'Broccoli'), ('Lemon', 0.75, 'Lemon'), 
        ('Limes', 0.60, 'Lime (fruit)'), ('Navel Oranges', 1.80, 'Orange (fruit)'),
        # Replacements (using commons search prefixes)
        ('Potatoes (5 lb)', 4.20, 'COMMONS:raw potatoes'),
        ('Garlic (3 pack)', 1.50, 'COMMONS:garlic bulbs'),
        ('Cherry Tomatoes', 2.99, 'COMMONS:cherry tomatoes'),
    ][:10], # Strictly keep 10 items
    
    'dairy-bread': [
        ('Whole Milk', 3.99, 'Milk'), ('Large White Eggs', 4.19, 'COMMONS:white eggs carton'), ('Unsalted Butter', 5.99, 'Butter'),
        ('Cheddar Cheese Block', 4.50, 'Cheddar cheese'), ('Shredded Mozzarella', 4.99, 'Mozzarella'),
        ('Greek Yogurt', 1.25, 'Yogurt'), ('Cream Cheese', 2.49, 'Cream cheese'), ('Sour Cream', 2.10, 'Sour cream'),
        ('White Bread Loaf', 2.49, 'Bread'), ('Croissants', 4.99, 'Croissant'),
    ][:10],
    
    'snacks-drinks': [
        ('Potato Chips', 3.99, 'COMMONS:bowl of potato chips'), ('Tortilla Chips', 4.50, 'COMMONS:tortilla chips'), ('Pretzels', 2.99, 'Pretzel'),
        ('Popcorn', 3.20, 'Popcorn'), ('Mixed Nuts', 6.99, 'Mixed nuts'), ('Chocolate Chip Cookies', 3.50, 'Chocolate chip cookie'),
        ('Gummy Bears', 2.50, 'Gummy bear'), ('Dark Chocolate Bar', 2.99, 'Chocolate'), ('Cola (12 Pack)', 6.99, 'Cola'),
        ('Orange Juice', 4.50, 'Orange juice'),
    ][:10],
    
    'meat-fish': [
        ('Ground Beef', 5.99, 'Ground beef'), ('Chicken Breasts', 7.50, 'COMMONS:raw chicken breast'), ('Bacon', 6.99, 'Bacon'),
        ('Pork Chops', 6.50, 'Pork chop'), ('Steak', 12.99, 'COMMONS:raw beef steak'), ('Sausages', 5.99, 'COMMONS:raw sausages'),
        ('Turkey Breast', 6.50, 'COMMONS:sliced turkey meat'), ('Ham', 5.50, 'Ham'), ('Salmon Fillet', 10.99, 'COMMONS:raw salmon fillet'),
        ('Shrimp', 9.99, 'COMMONS:raw shrimp'),
    ][:10],
    
    'cleaning': [
        ('Paper Towels', 10.99, 'Paper towel'), ('Dish Soap', 3.49, 'Dishwashing liquid'), ('Laundry Detergent', 12.99, 'Laundry detergent'),
        ('Fabric Softener', 6.50, 'COMMONS:fabric softener bottle'), ('All-Purpose Cleaner', 4.20, 'Cleaning agent'), ('Bleach', 4.99, 'Bleach'),
        ('Wet Wipes', 5.50, 'Wet wipe'), ('Broom', 14.99, 'Broom'), ('Mop', 12.50, 'Mop'), ('Sponges', 4.50, 'Sponge (tool)'),
    ][:10],
    
    'bath-body': [
        ('Body Wash', 6.99, 'Shower gel'), ('Shampoo', 7.50, 'COMMONS:shampoo bottle'), ('Conditioner', 7.50, 'Hair conditioner'),
        ('Bar Soap', 4.99, 'Soap'), ('Toothpaste', 3.99, 'Toothpaste'), ('Toothbrush', 4.50, 'Toothbrush'),
        ('Mouthwash', 5.50, 'Mouthwash'), ('Deodorant', 5.99, 'COMMONS:deodorant stick'), ('Body Lotion', 8.50, 'Lotion'),
        ('Hand Sanitizer', 2.50, 'Hand sanitizer'),
    ][:10],
    
    'paper-goods': [
        ('Toilet Paper', 12.99, 'Toilet paper'), ('Facial Tissues', 2.50, 'Facial tissue'), ('Paper Plates', 4.50, 'COMMONS:paper plates'),
        ('Paper Cups', 3.99, 'Paper cup'), ('Napkins', 3.50, 'Napkin'), ('Aluminum Foil', 4.99, 'Aluminium foil'),
        ('Plastic Wrap', 3.50, 'Plastic wrap'), ('Parchment Paper', 4.20, 'Parchment paper'), ('Zipper Bags', 3.99, 'Zipper storage bag'),
        ('Coffee Filters', 2.99, 'Coffee filter'),
    ][:10],
    
    'pet-care': [
        ('Dog Food (Dry)', 24.99, 'Dog food'), ('Cat Food (Dry)', 14.99, 'Cat food'), ('Dog Biscuits', 5.99, 'Dog biscuit'),
        ('Cat Litter', 12.99, 'COMMONS:cat litter'), ('Pet Shampoo', 7.99, 'COMMONS:pet shampoo'), ('Dog Collar', 12.50, 'COMMONS:dog collar'),
        ('Leash', 14.99, 'Leash'), ('Fish Food', 4.99, 'COMMONS:fish food flakes'), ('Bird Seed', 7.50, 'COMMONS:bird seed'), ('Hamster', 6.50, 'Hamster'),
    ][:10]
}

def get_commons_image(search_term):
    """Search Wikimedia Commons for a specific image file to avoid abstract Wikipedia articles"""
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(search_term)}&srnamespace=6&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PyShop/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            results = data.get('query', {}).get('search', [])
            for res in results:
                title = res['title']
                if title.lower().endswith(('.jpg', '.png', '.jpeg')):
                    # Fetch the URL for this specific file
                    file_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
                    file_req = urllib.request.Request(file_url, headers={'User-Agent': 'PyShop/1.0'})
                    file_data = json.loads(urllib.request.urlopen(file_req).read())
                    pages = file_data['query']['pages']
                    return list(pages.values())[0]['imageinfo'][0]['url']
    except Exception as e:
        print(f"Failed to fetch from Commons {search_term}: {e}")
    return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

def get_wikimedia_image(title):
    if title.startswith('COMMONS:'):
        return get_commons_image(title.replace('COMMONS:', ''))
        
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={urllib.parse.quote(title)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PyShop/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if 'original' in page_data:
                    return page_data['original']['source']
    except Exception as e:
        print(f"Failed to fetch {title}: {e}")
    # Fallback
    return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

def seed():
    print("Deleting old products...")
    Product.objects.all().delete()
    
    added_count = 0
    print("Fetching strictly 10 items per category (80 products total) from Wikimedia...")
    
    for category, items in CATEGORIES.items():
        for name, price, wiki_title in items:
            img_url = get_wikimedia_image(wiki_title)
            
            Product.objects.create(
                name=name,
                price=price,
                stock=random.randint(20, 100),
                image_url=img_url,
                category=category
            )
            added_count += 1
            print(f"Added {added_count}/80: {name} via {wiki_title}")
            time.sleep(0.1)
                
    print(f"Successfully created {added_count} products!")

if __name__ == '__main__':
    seed()
