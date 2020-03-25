from django.contrib import admin
from .models import Game, Collection, Photo

# Register your models here.
admin.site.register(Game)
admin.site.register(Collection)
admin.site.register(Photo)