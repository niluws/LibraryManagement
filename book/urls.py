from django.urls import path
from . import views

urlpatterns = [
    path('borrow-book/', views.BookBorrowView.as_view(), name='borrow-book'),
    path('return/<int:id>/', views.ReturnBookView.as_view(), name='return-book'),
    path('customer-book/', views.CustomerBookListView.as_view(), name='customer-book-list'),
    path('post-book/', views.PostBookView.as_view(), name='post-book'),
    path('book/', views.BookListView.as_view(), name='book-list'),
    path('income-report/', views.IncomeReportView.as_view(), name='income-report'),
]
