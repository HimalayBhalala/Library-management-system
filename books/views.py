from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from users.permission import IsLibrarian,IsStudent
from .serializers import BookSerializer,ReadBookSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Book,ReadBook
from rest_framework.exceptions import NotFound
from authentication.models import User
from users.filters import FilterByBookName
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from datetime import date


# Create your views here.

class GetAllBook(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filterset_class = FilterByBookName
    search_fields = ["name"]
    

@api_view(["POST"])
@permission_classes([IsLibrarian])
def add_book(request):
    if request.method == "POST":
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Data added successfully","data":serializer.data})


@api_view(["PUT","PATCH"])
@permission_classes([IsLibrarian])
def update_book(request,id):
    try:
        book = Book.objects.get(id=id)
        if request.method == "PATCH":
            serializer = BookSerializer(book,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"Book update successfully"})
            else:
                return Response({"message":"Enter a valid detail"})
        if request.method == "PUT":
            serializer = BookSerializer(book,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"Book update successfully"})
            else:
                return Response({"message":"Enter a valid detail"})
    except Book.DoesNotExist:
        raise NotFound("No book found using this id ")
    
@api_view(["PATCH"])
@permission_classes([IsLibrarian])
def librarian_issued_book_to_student(request,student_id,book_id):
    try:
        student = User.objects.get(id=student_id)
        book = Book.objects.get(id=book_id)
        book_record = ReadBook.objects.filter(student=student,book=book,
        student_issued=True,librarian_issued=False)
        if book_record:
            for data in book_record:
                data.librarian_issued_book()
            serializer = ReadBookSerializer(book_record,many=True)
            return Response({"data":serializer.data})
        else:
            return Response({"message":"Librarian can have already issue "})
    except ReadBook.DoesNotExist:
        raise NotFound("Data is not found")

@api_view(["DELETE"])
@permission_classes([IsLibrarian])
def delete_book(request,id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return Response({"message":"Book deleted successfully..."})
    except Book.DoesNotExist:
        raise NotFound("No book found using this id ")
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_one_book(request,id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book)
        return Response({"book":serializer.data})
    except Book.DoesNotExist:
        raise NotFound("No book found using this id ")
    

@api_view(["GET"])
@permission_classes([IsLibrarian])
def get_record_of_all_issue_book(request):
    record = ReadBook.objects.all()
    serializer = ReadBookSerializer(record,many=True)
    return Response({"data":serializer.data})


@api_view(["POST"])
@permission_classes([IsStudent])
def get_read_book(request,book_id):
    try:
        student_id = request.user.id
        student = User.objects.get(id=student_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise NotFound("Book is not in list")
    if ReadBook.objects.filter(student=student,book=book,returned=False):
        return Response({"message":"Book is already exist."})
    else:
        ReadBook.objects.create(student=student,book=book,student_issued=True,student_issued_at=date.today())
    return Response({"messege":"Book added successfully..."})
    

@api_view(["GET"])
@permission_classes([IsStudent])
def student_show_read_book(request):
    student_id = request.user.id
    student = User.objects.get(id=student_id)
    book_record = ReadBook.objects.filter(student=student,student_issued=True,librarian_issued=True)
    serializer = ReadBookSerializer(book_record,many=True)
    return Response({"data":serializer.data})


@api_view(["PATCH"])
@permission_classes([IsStudent])
def student_return_book(request,book_id):
    try:
        student_id = request.user.id
        student = User.objects.get(id=student_id)
        book = Book.objects.get(id=book_id)
        book_record = ReadBook.objects.filter(student=student,book=book,returned=False,librarian_issued=True)
        if book_record:
            for record in book_record:
                record.book_retuned()
            serializer = ReadBookSerializer(book_record,many=True)
            return Response({"data":serializer.data})
        else:
            return Response({"message":"Book is already returned"})
    except Book.DoesNotExist:
        raise NotFound("Book is not found")
    