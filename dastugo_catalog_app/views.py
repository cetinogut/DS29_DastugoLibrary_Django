from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,  HttpResponseRedirect
from .models import Book, Author, BookInstance, Genre
from django.views import generic #
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# form view and modalform view for renewal
import datetime
from django.urls import reverse
# from dastugo_catalog_app.forms import RenewBookForm
from dastugo_catalog_app.forms import RenewBookModelForm
from django.contrib.auth.decorators import login_required, permission_required

# author and book CRUD views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from dastugo_catalog_app.models import Author

# Create your views here.

""" def home(request):
   #return HttpResponse("<h1>Welcome to Dastugo Catalog Local Library Application</h1>")
   return render(request, "dastugo_catalog_app/home.html") """


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    
    # Available genres (containing = 'Science')
    num_genres_B = Genre.objects.filter(name__startswith='B').count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres_B' :num_genres_B,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'dastugo_catalog_app/index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    #template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    
    #def get_queryset(self):
     #   return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    
    """ def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'dastugo_catalog_app/book_detail.html', context={'book': book}) """

class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='dastugo_catalog_app/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
class AllLoanedBooksForLibrarianListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'dastugo_catalog_app.can_mark_returned'
    template_name ='dastugo_catalog_app/bookinstance_list_all_borrowed_librarian.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    
@login_required
@permission_required('dastugo_catalog_app.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        #form = RenewBookForm(request.POST) #developer form first then used A ModelForm below
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_instance.due_back = form.cleaned_data['renewal_date'] #developed form first then used A ModelForm below
            book_instance.due_back = form.cleaned_data['due_back'] 
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed-books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        #form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})#developed form first then used A ModelForm below
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'dastugo_catalog_app/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors') # on delete redirect to authors list