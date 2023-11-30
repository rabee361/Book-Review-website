from rest_framework.response import Response
from bookapp.models import Book , Review , Author , Genre
from rest_framework.views import APIView
from .serializers import BookSerializer , ReviewSerializer , AuthorSerializer , GenreSerializer
from rest_framework.generics import ListAPIView , RetrieveAPIView , UpdateAPIView
from bookapp.filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class CustomPagination(PageNumberPagination):
    page_size = 1


class GetBooks(ListAPIView):
    queryset = Book.objects.prefetch_related('author','genre','quotes').all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


class GetBook(RetrieveAPIView):
    queryset = Book.objects.prefetch_related('author','genre','quotes').all()
    serializer_class = BookSerializer


class GetGenres(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GetAuthor(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class RelatedBooks(APIView):
    def get(self,request,pk):
        book = Book.objects.prefetch_related('author','quotes','genre').get(id=pk)
        genres = [i.name for i in book.genre.all()]
        books = Book.objects.prefetch_related('author','quotes','genre')\
                            .filter(Q(genre__name__in=genres))\
                            .exclude(name=book.name).distinct()
        
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

#-----another way using generic view-----#
class RelatedBooks2(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    
    def get(self,request,pk):
        self.object = self.get_object()
        book = Book.objects.prefetch_related('author','quotes','genre').get(id=pk)
        genres = [i.name for i in self.object.genre.all()]
        books = Book.objects.prefetch_related('author','quotes','genre')\
                            .filter(Q(genre__name__in=genres))\
                            .exclude(name=self.object.name).distinct()
        
        serializer = self.get_serializer(books,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
