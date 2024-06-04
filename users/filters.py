import django_filters
from books.models import Book

class FilterByBookName(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Book
        fields = ["name"]