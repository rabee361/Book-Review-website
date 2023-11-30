from django.urls import path
from .views import GetBooks , GetBook , GetGenres , GetAuthor , RelatedBooks2

urlpatterns = [
    path('all_books/' , GetBooks.as_view() , name="books"),
    path('book/<str:pk>/' , GetBook.as_view() , name="single_book"),
    path('genres/' , GetGenres.as_view() , name="genres"),
    path('author/<str:pk>' , GetAuthor.as_view() , name="author"),
    path('related_books/<str:pk>' , RelatedBooks2.as_view() , name="related_books")
]