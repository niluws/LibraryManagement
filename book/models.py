from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


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
    max_borrow_days = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        n = self.stock
        if n == 0:
            self.max_borrow_days = 3
        else:
            f_30 = Transaction.objects.filter(book=self, date__gte=timezone.now() - timedelta(days=30)).count()
            result = (30 * n) / (n + f_30) + 1
            self.max_borrow_days = max(result, 3)

        super().save(*args, **kwargs)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    borrowed_books = models.ManyToManyField(Book, through='Transaction')
    max_borrow_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


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
    date = models.DateField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
