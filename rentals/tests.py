from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Rental
from datetime import timedelta
from django.utils import timezone

class BookModelTest(TestCase):
    def test_monthly_fee_calculation(self):
        book = Book.objects.create(
            title="Test Book",
            author = "Author",
            page_count = 300
        )
        self.assertEqual(book.monthly_fee(), 3)


class RentalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username = "username",
            password = "password@123"
        )

        self.book = Book.objects.create(
            title="Rental book",
            author= "Author",
            page_count=300
        )

        self.rental = Rental.objects.create(
            user=self.user,
            book=self.book,
            start_date=timezone.now().date() - timedelta(days=60),
            due_date=timezone.now().date() - timedelta(days=30),
            total_fee=0
        )

    def test_fee_after_free_period(self):
        self.rental.calculate_fee()
        self.assertGreater(self.rental.total_fee, 0)

    def test_extend_rental(self):
        old_due_date = self.rental.due_date
        self.rental.extend_rental()
        self.assertGreater(self.rental.due_date, old_due_date)


# Create your tests here.
