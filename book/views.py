from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Book, Customer, Transaction
from .serializers import TransactionSerializer
from .tasks import deduct_daily_rent


class BookBorrowView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = request.data.get('customer')
        book_id = request.data.get('book')

        customer = get_object_or_404(Customer, id=customer_id)
        book = Book.objects.get(id=book_id)

        existing_transaction = customer.transaction_set.filter(return_date=None).exists()
        borrowed_from_category = customer.transaction_set.filter(
            book__category_id=book.category.id,
            customer_id=customer_id

        ).count()
        if existing_transaction:
            return Response({'error': 'You already have borrowed a book.Return the book first and try again.'},
                            status=status.HTTP_400_BAD_REQUEST)

        elif customer.account_balance < book.category.daily_price * 3:
            return Response({'error': 'Insufficient balance to borrow the book.'}, status=status.HTTP_400_BAD_REQUEST)
        elif book.stock == 0:
            return Response({'error': 'book does not exist.'})
        elif borrowed_from_category > customer.max_borrow_limit:
            return Response({'error': 'More than your limit.You can borrow from other category.'},
                            status=status.HTTP_400_BAD_REQUEST)

        deduct_daily_rent()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReturnBookView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        print(request.data.get('calculate_late_days'))
        self.perform_update(serializer)
        return Response(serializer.data)
