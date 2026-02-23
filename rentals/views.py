from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import Book, Rental
from .services import fetch_book_from_openlibrary

from rest_framework.generics import ListAPIView
from .serializers import RentalSerializer

class CreateRentalView(APIView):
    def post(self, request):
        username = request.data.get("username")
        title = request.data.get("title")

        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error":"user not found"}, status=404)


        book_info = fetch_book_from_openlibrary(title)
        if not book_info:
            return Response({"error":"Book not found"}, status=404)

        book, _ = Book.objects.get_or_create(
            title=book_info["title"],
            defaults={
                "author": book_info["author"],
                "page_count": book_info["page_count"],
            }
        )

        rental = Rental.objects.create(
            user=user,
            book=book,
            start_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=30),
        )

        return Response({
            "message": "Rental created successfully",
            "monthly_fee_after_free_month": book.monthly_fee(),
            "rental_id": rental.id,
        })

class RentalListView(ListAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

class ExtendRentalView(APIView):

    def post(self, request, rental_id):
        rental = Rental.objects.filter(id=rental_id).first()

        if not rental:
            return Response({"error": "Rental not found"}, status=404)

        rental.extend_rental(months=1)

        return Response({
            "message": "Rental extended by 1 month",
            "new_due_date": rental.due_date,
            "total_fee": rental.total_fee,
        })