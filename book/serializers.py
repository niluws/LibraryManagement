from rest_framework import serializers
from .models import Transaction, Book


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
        fields = ['title', 'category', 'stock', 'times_borrowed', 'borrowers']


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
