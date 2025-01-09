from django.core.management.base import BaseCommand
from blog.models import Category

class Command(BaseCommand):
    help = 'Creates initial blog categories'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Technology',
                'description': 'Posts about programming, software, and tech news'
            },
            {
                'name': 'Travel',
                'description': 'Travel experiences and tips'
            },
            {
                'name': 'Lifestyle',
                'description': 'Posts about daily life, health, and wellness'
            },
            {
                'name': 'Food',
                'description': 'Recipes, restaurant reviews, and cooking tips'
            },
        ]

        for category in categories:
            Category.objects.get_or_create(
                name=category['name'],
                defaults={'description': category['description']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{category["name"]}"')
            )