from django import forms
from .models import issued_books

class BookForm(forms.ModelForm):
    class Meta:
        model = issued_books
        fields = ['book_id','book_name', 'author_name', 'edition', 'genre']