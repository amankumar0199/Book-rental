from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import math
from decimal import Decimal

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    page_count = models.IntegerField()

    def monthly_fee(self):
        return Decimal(self.page_count) / Decimal(100)

    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    start_date = models.DateField(default=timezone.now, null=False, blank=False)
    due_date = models.DateField(blank=True, null=False)

    total_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    returned = models.BooleanField(default=False)


    FREE_DAYS = 30

    def save(self, *args, **kwargs):
        # Set due date automatically for first rental
        if not self.due_date:
            self.due_date = self.start_date + timedelta(days=self.FREE_DAYS)
        super().save(*args, **kwargs)

    def calculate_fee(self):
        if not self.start_date:
            return 0

        today = timezone.now().date()
        days_used = (today - self.start_date).days

        if days_used <= self.FREE_DAYS:
            return 0

        extra_days = days_used - self.FREE_DAYS
        extra_months = math.ceil(extra_days / 30)

        return round(extra_months * self.book.monthly_fee(), 2)

    def extend_rental(self, months=1):
        self.due_date += timedelta(days=30 * months)
        additional_fee = Decimal(months) * self.book.monthly_fee()
        self.total_fee += additional_fee
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"





