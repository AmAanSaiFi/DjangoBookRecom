# recommender/management/commands/load_books.py
from django.core.management.base import BaseCommand
from recommender.models import Book
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "C:/Users/Amaan Saifi/Downloads/data.csv" 
        df = pd.read_csv(url, error_bad_lines=False)
        # df.head()
        selected_features = ['title','authors','categories','description']
        # Replacing the null values with null string
        for feature in selected_features:
            df[feature] = df[feature].fillna('')
        # df.head()
        df_filtered = df[selected_features]
        Book.objects.bulk_create(Book(**data) for data in df_filtered.to_dict('records'))
        self.stdout.write(self.style.SUCCESS('Books loaded successfully!'))
