from django.db import models
from django.core.exceptions import ValidationError
import os
class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField()

    def __str__(self):
        return self.name

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Только PDF-файлы разрешены.')

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    description = models.TextField()
    publication_year = models.PositiveIntegerField()
    file = models.FileField(upload_to='books/')

    def clean(self):
        super().clean()
        file = self.file
        if file:
            extension = os.path.splitext(file.name)[1].lower()
            if extension not in ['.pdf', '.txt']:
                raise ValidationError("Разрешены только файлы PDF и текстовые файлы.")
    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    text = models.TextField()
    user_name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_name} - {self.rating}'

