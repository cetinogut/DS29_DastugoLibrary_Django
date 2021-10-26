from django.contrib import admin
#from .models import Genre, Author, Book, BookInstance
from .models import Genre, Language, Author, Book, BookInstance

# Register your models here. This is the simples way.. We have complex method as well shown below
admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(Author)
#admin.site.register(Book)
#admin.site.register(BookInstance)

# Inline editing of associated records
class BooksInline(admin.TabularInline): # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site#inline_editing_of_associated_records
    model = Book
    extra = 0 

# Define the admin class for admin site customization
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    empty_value_display = 'not dead'
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]



# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin) # created a new admin class for book above and registered in a classical way here

# Inline editing of associated records
class BooksInstanceInline(admin.TabularInline): # Sometimes it can make sense to be able to add associated records at the same time. For example, it may make sense to have both the book information and information about the specific copies you've got on the same detail page.
                                                ## You can do this by declaring inlines, of type TabularInline (horizontal layout) or StackedInline (vertical layout, just like the default model layout). You can add the BookInstance information inline to our Book detail by specifiying inlines in your BookAdmin:
    model = BookInstance
    extra = 0 # It would be better to have NO spare book instances by default and this can be done by setting the extra attribute to 0 in BooksInstanceInline model,
    
# Register the Admin classes for Book using the decorator
@admin.register(Book) # this decorator registers both Book and BookAdmin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )