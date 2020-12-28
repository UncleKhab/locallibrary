from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
# Create your views here.

def index(request):
    """View Function for home page"""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_fiction = Book.objects.filter(genre__name__icontains='fiction').filter(title__icontains='harry').count()

    # Available books ( status="a" )
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # the 'all()' is impled by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fiction': num_fiction,
    }

    return render(request, 'index.html', context=context)