from rest_framework import serializers
from .models import Book,ReadBook
from users.serializers import UserSerializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id","name","description","author","uploaded","info"]
        extra_kwargs = {"uploaded":{"read_only":True},"id":{"read_only":True},
                        "info":{"read_only":True}}
        

class ReadBookSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    book = BookSerializer()
    class Meta:
        model = ReadBook
        fields = "__all__"



