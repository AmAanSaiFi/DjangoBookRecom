from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.impute import SimpleImputer
from collections import defaultdict
import re

from .models import Book  # Import the Book model from recommender.models

def pre_process_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove non-alphanumeric characters
    return text

def create_tfidf_matrix(books):

    combined_features = [
        f"{book['title']} {book['authors']} {book['categories']} {book['description']}"
        for book in books
    ]
    combined_features = list(map(pre_process_text, combined_features))

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    return feature_vectors

def recommend_books(book_name):

    books = Book.objects.values('title', 'authors', 'categories', 'description').all()
    books_list = [book for book in books]  # Convert queryset to list

    tfidf_matrix = create_tfidf_matrix(books_list)

    user_book_index = [
        i
        for i, book in enumerate(books_list)
        if pre_process_text(book['title']) == pre_process_text(book_name)
    ]

    if not user_book_index:
        return []  # Handle case where book is not found

    similarity_scores = cosine_similarity(tfidf_matrix)[user_book_index[0]]
    sorted_similar_books = sorted(
        enumerate(similarity_scores), key=lambda x: x[1], reverse=True
    )

    recommendations = []
    for book_index, score in sorted_similar_books[1:]:  # Exclude user's book
        recommended_book = books_list[book_index]
        recommendations.append({'title': recommended_book['title'], 'score': score})

    return recommendations[:10]  # Return top 10 recommendations
