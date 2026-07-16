from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
from pathlib import Path
from django.contrib.auth.hashers import make_password
import re

from core.models import Restaurant, Review, CustomUser

from datetime import datetime

APP_DIR = Path(settings.BASE_DIR).resolve().parent

class Command(BaseCommand):
    help = 'Import data from a CSV file'

    #def add_arguments(self, parser):
    #		parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        restaurant_file_path = APP_DIR / 'data/restaurants.csv'
        review_file_path = APP_DIR / 'data/reviews.csv'
        user_file_path = APP_DIR / 'data/users.csv'

        #Import datasets
        restaurant_df = pd.read_csv(restaurant_file_path)
        review_df = pd.read_csv(review_file_path)
        user_df = pd.read_csv(user_file_path)

        #Converts review date to datetime
        review_df['date'] = pd.to_datetime(
                review_df['date'],
                errors='coerce'
        )

        restaurant_sample = restaurant_df.nlargest(20000, 'review_count').fillna(0)
        review_sample = review_df[review_df['business_id'].isin(restaurant_sample['business_id'])]
        #Selects at most 20 ratings for each recipe
        review_sample = review_sample.groupby('business_id').apply(lambda x: x.nlargest(20, 'date')).reset_index().drop(columns = 'level_1')

        user_sample = user_df[user_df['user_id'].isin(review_sample['user_id'])]

        user_sample['password'] = make_password('1234')

        self.stdout.write(self.style.NOTICE(datetime.now().strftime('%H:%M:%S') + " Beginning user import"))

        #Populates user table using all recipe and review authors
        user_instances = [
                CustomUser(
                        pk = row.user_id,
                        username = row.name,
                        password = row.password,
                )
                for row in user_sample.itertuples(index=False)
        ]

        CustomUser.objects.bulk_create(
                user_instances,
                ignore_conflicts=True,
                batch_size=5000,
        )

        self.stdout.write(datetime.now().strftime('%H:%M:%S') + self.style.SUCCESS('Successfully imported user data'))

        #Selects all review author user objects
        users = CustomUser.objects.in_bulk(field_name='id')

        self.stdout.write(self.style.NOTICE(datetime.now().strftime('%H:%M:%S') + " Beginning restaurant import"))

        #Populates recipe table using CSV data
        restaurant_instances = [
                Restaurant(
                        pk = row.business_id,
                        name = row.name,
                        address = row.address,
                        city = row.city,
                        state = row.state,
                        postal_code = row.postal_code,
                        latitude = row.latitude,
                        longitude = row.longitude,
                        stars = row.stars,
                        review_count = row.review_count,
                        is_open = row.is_open,
                        attributes = row.attributes,
                        categories = row.categories,
                        hours = row.hours,
                )
                for row in restaurant_sample.itertuples(index=False)
        ]

        Restaurant.objects.bulk_create(
                restaurant_instances,
                ignore_conflicts=True,
                batch_size=5000,
        )

        self.stdout.write(datetime.now().strftime('%H:%M:%S') + self.style.SUCCESS('Successfully imported restaurant data'))

        #Selects all recipes
        restaurants = Restaurant.objects.in_bulk(field_name='id')

        self.stdout.write(self.style.NOTICE(datetime.now().strftime('%H:%M:%S') + " Beginning review import"))

        review_instances = [
                Review(
                        pk = row.review_id,
                        user = users.get(row.user_id),
                        business = restaurants.get(row.business_id),
                        rating = row.stars,
                        useful = row.useful,
                        funny = row.funny,
                        cool = row.cool,
                        review = row.text,
                        date = row.date,
                )
                for row in review_sample.itertuples(index=False)
        ]

        Review.objects.bulk_create(
                review_instances,
                ignore_conflicts=True,
                batch_size=5000,
        )

        self.stdout.write(datetime.now().strftime('%H:%M:%S') + self.style.SUCCESS('Successfully imported review data'))