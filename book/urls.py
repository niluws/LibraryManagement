from django.urls import path
from .views import BookBorrowView

urlpatterns = [
    path('borrow-book/', BookBorrowView.as_view(), name='borrow-book'),
]
