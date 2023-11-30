from rest_framework import serializers
from bookapp.models import Book , Author , Review , Genre ,Quote


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

   
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name','image']


class QuoteSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['text']

    #-----to return value without keys----#
    def to_representation(self, instance): 
        representation = super().to_representation(instance)
        return representation['text']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

    #-----to return the values as a list----#
    def to_representation(self, instance): 
        representation = super().to_representation(instance)
        return representation['name']
    


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True,read_only=True)
    quotes = QuoteSerialzier(many=True,read_only=True)
    genre = GenreSerializer(many=True , read_only=True)
    class Meta:
        model = Book
        fields  = ['name','author','cover','file','quotes','genre']





