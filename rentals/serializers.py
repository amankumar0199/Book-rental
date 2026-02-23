from rest_framework import serializers
from .models import Rental


class RentalSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)
    current_fee = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = [
            "id",
            "username",
            "book_title",
            "start_date",
            "due_date",
            "total_fee",
            "current_fee",
            "returned",
        ]

    def get_current_fee(self, obj):
        return obj.calculate_fee()
