import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm
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

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Check if the method is post and validate data. Return to the all borrowed page is everything goes right.
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    # If this is the first instance of loading the page, create the form and add a date 3 weeks from current date into the due_date field.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)