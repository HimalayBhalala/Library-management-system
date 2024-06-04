from django.urls import path
from . import views

urlpatterns = [
    path("add/",views.add_book,name="add-book"),
    path("all/",views.GetAllBook.as_view(),name="all-book"),
    path("update/<int:id>/",views.update_book,name="update-book"),
    path("delete/<int:id>/",views.delete_book,name="delete-book"),
    path("get/<int:id>/",views.get_one_book,name="one-book"),
    path("record/",views.get_record_of_all_issue_book,name="record-book"),
    path("student/get/<int:book_id>/",views.get_read_book,name="read-book"),
    path("student/get_book_record/",views.student_show_read_book,name="student-book-record"),
    path("student/return/<int:book_id>/",views.student_return_book,name="return-book")
]
