from django.urls import path
from .views import Books , SingleBook , GetGenres , GetAuthor

urlpatterns = [
    path('all_books/' , Books.as_view() , name="books"),
    path('book/<str:pk>/' , SingleBook.as_view() , name="single_book"),
    path('genres/' , GetGenres.as_view() , name="genres"),
    path('author/<str:pk>' , GetAuthor.as_view() , name="author")
]