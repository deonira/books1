from django import forms
from .models import Book, Author, Review
from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'publication_year', 'file', 'author']

    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label='Автор')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            extension = file.name.split('.')[-1].lower()
            if extension not in ['pdf', 'txt']:
                raise forms.ValidationError("Разрешены только файлы PDF и текстовые файлы.")
        return file

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')

        if title and author:
            if Book.objects.filter(title=title, author=author).exists():
                raise ValidationError('Книга с таким названием уже существует у выбранного автора.')

        return cleaned_data

class BookSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Поиск по книге')

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'biography']
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class AuthorSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Поиск по автору')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'user_name']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
        }