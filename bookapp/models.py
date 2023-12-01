from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator , MaxLengthValidator


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100  ,db_index=True)
    about = models.TextField(default="test")
    image = models.ImageField(upload_to='authors/' , null=True , default='None')

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.text[:50]}...'



class Book(models.Model):
    LANGUAGES = (
        ('en' , 'English'),
        ('ar' , 'Arabic')
    )
    name = models.CharField(max_length=150 , db_index=True)
    story = models.TextField(max_length=300 ,default="n")
    cover = models.ImageField(upload_to='covres/')
    author = models.ManyToManyField(Author)
    pages = models.IntegerField(default=250)
    language = models.CharField(max_length=30,choices=LANGUAGES , default='en')
    # publish_date = models.DateField(auto_now_add=True)
    genre = models.ManyToManyField(Genre)
    file = models.FileField(upload_to='books/')
    quotes = models.ManyToManyField(Quote)

    def __str__(self):
        author_names = ", ".join([str(author) for author in self.author.all()])
        return f'{self.name} - {author_names}'



class Review(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    fav_quote = models.TextField(validators=[MaxLengthValidator(500)])
    text = models.TextField()
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.text[:50]}...'



class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, db_index=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.text[:50]}...'

