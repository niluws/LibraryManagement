from django.urls import path
from . import views

urlpatterns = [
    path('borrow-book/', views.BookBorrowView.as_view(), name='borrow-book'),
    path('return/<int:id>/', views.ReturnBookView.as_view(), name='return-book'),
]
