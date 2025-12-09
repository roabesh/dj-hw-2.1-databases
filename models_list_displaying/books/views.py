from django.shortcuts import render
from books.models import Book


def books_view(request, pub_date=None):
    template = 'books/books_list.html'
    
    if pub_date:
        # Get books for specific date
        books = Book.objects.filter(pub_date=pub_date.date())
        
        # Get previous and next dates
        previous_date = Book.objects.filter(pub_date__lt=pub_date.date()).order_by('-pub_date').first()
        next_date = Book.objects.filter(pub_date__gt=pub_date.date()).order_by('pub_date').first()
        
        context = {
            'books': books,
            'previous_date': previous_date.pub_date if previous_date else None,
            'next_date': next_date.pub_date if next_date else None,
        }
    else:
        # Get all books
        books = Book.objects.all()
        context = {
            'books': books,
        }
    
    return render(request, template, context)
