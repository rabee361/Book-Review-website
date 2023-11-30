from django.urls import path
from .views import GetBooks , GetBook , GetGenres , GetAuthor , RelatedBooks2 , SignUp2 , Login , Logout , WriteMessage

urlpatterns = [
    path('all_books/' , GetBooks.as_view() , name="books"),
    path('book/<str:pk>/' , GetBook.as_view() , name="single_book"),
    path('genres/' , GetGenres.as_view() , name="genres"),
    path('author/<str:pk>' , GetAuthor.as_view() , name="author"),
    path('related_books/<str:pk>' , RelatedBooks2.as_view() , name="related_books"),
    path('sign_up/', SignUp2.as_view() , name="sign_up"),
    path('login/' , Login.as_view() , name="login"),
    path('logout/' , Logout.as_view() , name="logout"),
    path('message/' , WriteMessage.as_view() , name="message")
]