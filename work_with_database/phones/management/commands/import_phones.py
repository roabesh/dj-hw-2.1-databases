import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    help = 'Import phones from CSV file'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone_data in phones:
            # Convert string to boolean
            lte_exists = phone_data['lte_exists'].lower() == 'true'
            
            # Convert string to date
            release_date = datetime.strptime(phone_data['release_date'], '%Y-%m-%d').date()
            
            # Create or update phone instance
            Phone.objects.update_or_create(
                id=int(phone_data['id']),
                defaults={
                    'name': phone_data['name'],
                    'price': float(phone_data['price']),
                    'image': phone_data['image'],
                    'release_date': release_date,
                    'lte_exists': lte_exists,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(phones)} phones'))
