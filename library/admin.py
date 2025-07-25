from django.contrib import admin
from .models import books, issued_books , users

# Register your models here.
admin.site.register(books)
admin.site.register(issued_books)
admin.site.register(users)
