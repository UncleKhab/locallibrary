from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
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

class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 10

# class CustomListView(generic.ListView):
#     model = Book   
#     context_object_name = 'my_book_list' # own name for the list as a template variable
#     queryset = Book.objects.filter(title__icontains='harry')[:5]
#     template_name = 'template_name_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    template_name='book_detail.html'

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'