from rest_framework import serializers
from bookapp.models import Book , Author , Review , Genre , Quote , Message
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password



   
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name','image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['name']



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
        fields  = ['name','author','cover','file','quotes','genre','language','pages']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['name']



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            return serializers.ValidationError("passwords don't match")
        validate_password(data['password'])
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        login(request,user)
        return user
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     return representation['username']




class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    class Meta:
        model = Message
        fields = ['user','text']

    def create(self, validated_data):
        request = self.context.get('request')
        msg = Message.objects.create(user=request.user,text=validated_data['text'])
        msg.save()
        return msg



class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    book = BookSerializer(many=False,read_only=True)
    book_name = serializers.CharField(write_only=True)
    class Meta:
        model = Review
        fields = ['user','book','book_name','fav_quote','text','stars']

    def create(self, validated_data):
        request = self.context.get('request')
        book_name = validated_data.pop('book_name')
        book = Book.objects.get(name=book_name)
        review = Review.objects.create(user=request.user,book=book , **validated_data)
        review.save()
        return review
    

