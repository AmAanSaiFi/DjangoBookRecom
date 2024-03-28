from django.shortcuts import render
from recommender.recommender import recommend_books

def get_recommendations(request):
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        try:
            recommendations = recommend_books(book_name)
            context = {'recommendations': recommendations}
            return render(request, 'recommendations.html', context)
        except ValueError:  # Handle potential errors during recommendation
            error_message = "Book not found or processing error occurred."
            context = {'error_message': error_message}
            return render(request, 'recommendations.html', context)
    else:
        context = {}
        return render(request, 'recommendations.html', context)
    # return HttpResponse("Hey this is a first page.")
