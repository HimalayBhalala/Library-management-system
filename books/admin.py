from django.contrib import admin
from .models import Book,ReadBook

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ["name","description","author","uploaded"]
admin.site.register(Book,BookAdmin)

class ReadBookAdmin(admin.ModelAdmin):
    list_display = ["student","book","student_issued","librarian_issued","student_issued_at","librarian_issued_at","returned","returned_at","fine"]
admin.site.register(ReadBook,ReadBookAdmin)
