from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

    #Session Counter
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # the 'all()' is impled by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fiction': num_fiction,
        'num_visits': num_visits,
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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksForLibrariansListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'bookinstante_list_borrowed_librarian.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')