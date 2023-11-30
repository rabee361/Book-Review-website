from rest_framework.response import Response
from bookapp.models import Book , Review , Author , Genre
from rest_framework.views import APIView
from .serializers import BookSerializer , ReviewSerializer , AuthorSerializer , GenreSerializer
from rest_framework.generics import ListAPIView , RetrieveAPIView
from bookapp.filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend


class Books(ListAPIView):
    queryset = Book.objects.prefetch_related('author','genre','quotes').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


class SingleBook(RetrieveAPIView):
    queryset = Book.objects.prefetch_related('author','genre','quotes').all()
    serializer_class = BookSerializer


class GetGenres(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GetAuthor(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer