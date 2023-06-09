import datetime

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import TextInput

from .models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm, RegisterUserForm


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    books_l = Book.objects.filter(title__icontains='la')
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0) #Here we first get the value of the 'num_visits' session key, setting the value to 0 if it has not previously been set.
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'books_l' : books_l,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    
    def get_queryset(self):
        return Book.objects.order_by('title')

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    
    def get_queryset(self):
        return Author.objects.order_by('last_name')
    
class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    
    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['date_of_birth'].widget.attrs['placeholder'] = 'dd-mm-aaaa'
        context['form'].fields['date_of_death'].widget.attrs['placeholder'] = 'dd-mm-aaaa'
        return context

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('books')
    
class RegisterView(generic.View):
    def post(self, *args, **kwargs):
        form = RegisterUserForm(self.request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            is_superuser = form.cleaned_data["is_superuser"]
            user = authenticate(username=username, password=password)
            if is_superuser == True:
                user.is_staff = True
                user.save()
            print(user.is_staff)
            login(self.request, user)
            return redirect("index")
        else:
            messages.error(self.request, "There was an error with your form")
            form = RegisterUserForm()
            return render(self.request, "catalog/register.html", {
                "form" : form
            })
        
    def get(self, *args, **kwargs):
        form = RegisterUserForm()
        context = {
            "form" : form
        }
        return render(self.request, "catalog/register.html", context)