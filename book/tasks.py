from celery import shared_task
from django.utils import timezone
from .models import Transaction


@shared_task
def deduct_daily_rent():
    today = timezone.now().date()
    ongoing_transactions = Transaction.objects.filter(
        return_date=None
    ).exclude(
        date__gt=today
    )

    for transaction in ongoing_transactions:
        customer = transaction.customer
        book = transaction.book
        daily_price = book.category.daily_price

        if transaction.transaction_type == Transaction.BOOK_BORROW:
            customer.account_balance -= daily_price
            customer.save()
