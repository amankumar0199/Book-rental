from django.contrib import admin
from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Book, Rental
from .services import fetch_book_from_openlibrary


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "page_count", "monthly_fee")



class RentalAdminForm(forms.ModelForm):
    book_title = forms.CharField(required=True, label="Book Title")

    class Meta:
        model = Rental
        fields = ["user", "book_title"]

    def save(self, commit=True):
        instance = super().save(commit=False)

        title = self.cleaned_data["book_title"]

        book_info = fetch_book_from_openlibrary(title)
        if not book_info:
            raise forms.ValidationError(
                f"Book '{title}' not found in OpenLibrary."
            )

        # getorcreate return tuple (Book_instance, true/false). True if new book is created and false if already exists.

        book, ifbookcreated = Book.objects.get_or_create(
            title=book_info["title"],
            defaults={
                "author": book_info["author"],
                "page_count": book_info["page_count"],
            },
        )

        instance.book = book
        instance.start_date = timezone.now().date()
        instance.due_date = timezone.now().date() + timedelta(days=30)
        instance.total_fee = 0

        if commit:
            instance.save()
            self.save_m2m()

        return instance


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    form = RentalAdminForm
    list_display = ("user", "book", "start_date", "due_date", "total_fee", "returned")
    list_filter = ("user", "returned")
    search_fields = ("user__username", "book__title")
    actions = ["extend_one_month"]

    def extend_one_month(self, request, queryset):
        for rental in queryset:
            rental.extend_rental(months=1)
        self.message_user(request, "Selected rentals extended by one month.")

    #restrict built-in change
    def has_change_permission(self, request, obj=None):
        return False  # Prevent editing existing rentals

    extend_one_month.short_description = "Extend rental by 1 month"







