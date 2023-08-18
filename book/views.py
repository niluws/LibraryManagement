from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Book, Customer
from .serializers import TransactionSerializer


class BookBorrowView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = request.data.get('customer')
        book_id = request.data.get('book')

        customer = get_object_or_404(Customer, id=customer_id)
        book = get_object_or_404(Book, id=book_id, stock__gt=0)

        existing_transaction = customer.transaction_set.filter(return_date=None).exists()
        if existing_transaction:
            return Response({'error': 'You already have borrowed a book.Return the book first and try again.'},
                            status=status.HTTP_400_BAD_REQUEST)

        elif customer.account_balance < book.category.daily_price * 3:
            return Response({'error': 'Insufficient balance to borrow the book.'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
