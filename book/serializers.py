from rest_framework import serializers
from .models import Transaction, Book,Category


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CustomerBookSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    times_borrowed = serializers.SerializerMethodField()
    borrowers = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'category', 'stock', 'times_borrowed','borrowers']

    def get_times_borrowed(self, obj):
        return obj.transaction_set.filter(transaction_type=Transaction.BOOK_BORROW).count()

    def get_borrowers(self, obj):
        borrowers = obj.transaction_set.filter(transaction_type=Transaction.BOOK_BORROW).values_list(
            'customer__user__username', flat=True)
        return list(borrowers)



class BookSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    times_borrowed = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'category', 'stock', 'times_borrowed']

    def get_times_borrowed(self, obj):
        return obj.transaction_set.filter(transaction_type=Transaction.BOOK_BORROW).count()


class PostBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['title','stock','price','category']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'genre', 'type')


class IncomeReportSerializer(serializers.Serializer):
    category = CategorySerializer()
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
