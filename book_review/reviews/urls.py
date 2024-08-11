from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.add_author, name='add_author'),
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),
    path('books/add/<int:author_id>/', views.add_book, name='add_book_with_author')
]