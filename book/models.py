from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)


class Category(models.Model):
    genre = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.genre} - {self.type}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    def max_borrow_days(self):
        n = self.stock
        f_30 = Transaction.objects.filter(book=self, borrow_date__gte=timezone.now() - timedelta(days=30)).count()
        result = (30 * n) / (n + f_30) + 1
        return max(result, 3)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    borrowed_books = models.ManyToManyField(Book, through='Transaction')
    max_borrow_limit = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.user.username

    def penalty(self):
        borrowed_books = Transaction.objects.filter(customer=self, return_date__isnull=True)
        penalty = sum((timezone.now() - borrow.date).days for borrow in borrowed_books if
                      (timezone.now() - borrow.date).days > borrow.book.max_borrow_days())
        return penalty

    def can_borrow(self):
        return self.borrowed_books.count() < self.max_borrow_limit

    def overdue_books(self):
        return Transaction.objects.filter(customer=self, return_date__isnull=True, date__lt=timezone.now() - timedelta(days=self.max_borrow_limit))


class Transaction(models.Model):
    BOOK_BORROW = 'BB'
    BOOK_PURCHASE = 'BP'
    TRANSACTION_TYPE_CHOICES = [
        (BOOK_BORROW, 'Book Borrow'),
        (BOOK_PURCHASE, 'Book Purchase'),
    ]

    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPE_CHOICES)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    return_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def is_overdue(self):
        return self.return_date is None and (timezone.now() - self.date).days > self.book.max_borrow_days()

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.book.price
        super().save(*args, **kwargs)
