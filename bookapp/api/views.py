from rest_framework.response import Response
from bookapp.models import Book , Review , Author , Genre
from rest_framework.views import APIView
from .serializers import BookSerializer , ReviewSerializer , AuthorSerializer , GenreSerializer , UserSerializer ,MessageSerializer
from rest_framework.generics import ListAPIView , RetrieveAPIView , CreateAPIView  ,ListCreateAPIView
from bookapp.filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.contrib.auth import login , logout , authenticate
from django.shortcuts import redirect

class CustomPagination(PageNumberPagination):
    page_size = 1


#-----get all books-----#
class GetBooks(ListAPIView):
    queryset = Book.objects.prefetch_related('author','genre','quotes').all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


#-----get single book-----#
class GetBook(RetrieveAPIView):
    queryset = Book.objects.prefetch_related('author','genre','quotes').all()
    serializer_class = BookSerializer



#----get all genres----#
class GetGenres(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


#------get a single author-----#
class GetAuthor(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


#-----get other books from the same genre or writer-----#
class RelatedBooks(APIView):
    def get(self,request,pk):
        book = Book.objects.prefetch_related('author','quotes','genre').get(id=pk)
        genres = [i.name for i in book.genre.all()]
        books = Book.objects.prefetch_related('author','quotes','genre')\
                            .filter(Q(genre__name__in=genres))\
                            .exclude(name=book.name).distinct()
        
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

#-----same as before but another way using generic view-----#
class RelatedBooks2(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    
    def get(self,request,pk):
        self.object = self.get_object()
        genres = [i.name for i in self.object.genre.all()]
        books = Book.objects.prefetch_related('author','quotes','genre')\
                            .filter(Q(genre__name__in=genres))\
                            .exclude(name=self.object.name).distinct()
        
        serializer = self.get_serializer(books,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
#-----sign up using apiview-----#
# class SignUp(APIView):
#     def post(self,request):
#         context = {'request':request}
#         serializer = UserSerializer(data=request.data , context=context)

#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-----sign up using generic view-----#
class SignUp2(CreateAPIView):
    serializer_class = UserSerializer



#-----login-----#
class Login(APIView):
    def get(self,request):
        return Response('hello , you can login here')
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username , password=password)
        if user:
            login(request,user)
            return redirect('books')
        return Response('error' , status=status.HTTP_404_NOT_FOUND)

#----logout----#
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        logout(request)
        return Response('done')


#-----user writing a message/complaint----#
class WriteMessage(CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]



class BookReviews(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        reviews = Review.objects.select_related('book','user').filter(book__id=pk)
        serializer = self.get_serializer(reviews,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

