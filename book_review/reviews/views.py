from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author, Review
from .forms import BookForm, BookSearchForm, AuthorForm, AuthorSearchForm, ReviewForm
from django.http import HttpResponse
from django.db import models
def book_list(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data.get('search')
        if search_term:
            books = books.filter(title__icontains=search_term)

    return render(request, 'book_list.html', {'books': books, 'form': form})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = ReviewForm()

    return render(request, 'book_detail.html', {
        'book': book,
        'reviews': reviews,
        'average_rating': average_rating,
        'form': form
    })

def home(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            new_author_name = request.POST.get('new_author_name', '')
            if new_author_name:
                new_author_biography = request.POST.get('new_author_biography', '')
                author, created = Author.objects.get_or_create(
                    name=new_author_name,
                    defaults={'biography': new_author_biography}
                )
                book.author = author
            else:
                book.author = form.cleaned_data.get('author')
            book.save()
            return redirect('home')
    else:
        form = BookForm()

    books = Book.objects.all()
    authors = Author.objects.all()

    return render(request, 'home.html', {'books': books, 'form': form, 'authors': authors})


def author_list(request):
    form = AuthorSearchForm(request.GET or None)
    authors = Author.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data.get('search')
        if search_term:
            authors = authors.filter(name__icontains=search_term)

    return render(request, 'author_list.html', {'authors': authors, 'form': form})
def add_book(request, author_id=None):
    author = None
    if author_id:
        author = get_object_or_404(Author, id=author_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            if author:
                book.author = author
            book.save()
            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form, 'author': author})


def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()

    return render(request, 'add_author.html', {'form': form})

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = Book.objects.filter(author=author)
    return render(request, 'author_detail.html', {'author': author, 'books': books})