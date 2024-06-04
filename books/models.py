from django.db import models
from datetime import datetime,timedelta
from authentication.models import User

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
    issued = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    returned_at = models.DateField(null=True,blank=True)
    fine = models.DecimalField(default=0.00,max_digits=2,
    max_length=5,decimal_places=2)

    def total_fine(self):
        total = 0.00
        if self.returned is False:
            days_diff = (datetime.now().date() - self.issued).days
            if days_diff > 7:
                total += 10 * (days_diff - 7)
        return total
        
    def save(self,*args, **kwargs):
        self.fine = self.total_fine()
        return super().save(*args, **kwargs)
    
    def book_retuned(self):
        if not self.returned:
            self.returned = True
            self.returned_at = datetime.now().date()
            self.save()
