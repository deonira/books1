from django.contrib import admin
from .models import Author, Book, Review
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'file')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'rating', 'user_name', 'approved')
    list_filter = ('approved',)
    search_fields = ('book__title', 'user_name', 'text')