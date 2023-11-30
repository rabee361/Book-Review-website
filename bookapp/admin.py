from django.contrib import admin
from .models import Book , Review , Author , Genre , Quote ,Message

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Quote)
admin.site.register(Message)
