from django.test import TestCase
from .models import Author, Book, Review
from django.urls import reverse
from django.http import HttpResponse
from .views import home, book_detail

class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Leo Tolstoy')

    def test_author_creation(self):
        self.assertEqual(self.author.name, 'Leo Tolstoy')
        self.assertTrue(isinstance(self.author, Author))
        self.assertEqual(str(self.author), 'Leo Tolstoy')

class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Leo Tolstoy')
        self.book = Book.objects.create(
            title='War and Peace',
            author=self.author,
            description='A historical novel.',
            publication_year=1869,
            file='path/to/book.pdf'
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, 'War and Peace')
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.description, 'A historical novel.')
        self.assertEqual(self.book.publication_year, 1869)
        self.assertEqual(self.book.file, 'path/to/book.pdf')

class ReviewModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Leo Tolstoy')
        self.book = Book.objects.create(
            title='War and Peace',
            author=self.author,
            description='A historical novel.',
            publication_year=1869,
            file='path/to/book.pdf'
        )
        self.review = Review.objects.create(
            book=self.book,
            rating=5,
            text='An amazing book!',
            user_name='John Doe',
            approved=True
        )

    def test_review_creation(self):
        self.assertEqual(self.review.book, self.book)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.text, 'An amazing book!')
        self.assertEqual(self.review.user_name, 'John Doe')
        self.assertTrue(self.review.approved)

class ViewsTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Leo Tolstoy')
        self.book = Book.objects.create(
            title='War and Peace',
            author=self.author,
            description='A historical novel.',
            publication_year=1869,
            file='path/to/book.pdf'
        )

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_book_detail_view_status_code(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')

    def test_book_detail_view_content(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book.pk}))
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.author.name)
        self.assertContains(response, self.book.description)
        self.assertContains(response, self.book.publication_year)

    def test_author_list_view_status_code(self):
        response = self.client.get(reverse('author_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author_list.html')

    def test_author_list_view_content(self):
        response = self.client.get(reverse('author_list'))
        self.assertContains(response, self.author.name)