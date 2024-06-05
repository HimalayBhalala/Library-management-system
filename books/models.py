from django.db import models
from datetime import datetime,timedelta
from authentication.models import User
from datetime import date

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    description = models.TextField(null=True,blank=True,default="This book is making smart your thing")
    author = models.CharField(max_length=100,null=False,blank=False)
    uploaded = models.DateField(auto_now_add=True)
    info = models.CharField(max_length=100,default="Give book after 7 days otherwise prepare to pay RS.10/day if issue date miss.")

    def __str__(self):
        return self.name
    

class ReadBook(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    student_issued = models.BooleanField(default=False)
    librarian_issued = models.BooleanField(default=False)
    student_issued_at = models.DateField(null=True,blank=True)
    librarian_issued_at = models.DateField(null=True,blank=True)
    returned = models.BooleanField(default=False)
    returned_at = models.DateField(null=True,blank=True)
    fine = models.IntegerField(default=0)

    def total_fine(self):
        total = 0
        if self.returned:
            days_diff = int((self.returned_at - self.librarian_issued_at).days)
            if days_diff > 7:
                total += 10 * (days_diff - 7)
        return total
    
    def book_retuned(self):
        if not self.returned:
            self.returned = True
            self.returned_at = datetime.now().date()
            self.fine = self.total_fine()
            self.save()

    def librarian_issued_book(self):
        if not self.librarian_issued:
            self.librarian_issued=True
            self.librarian_issued_at=date.today()
            self.save()