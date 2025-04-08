from django.contrib import admin
from .models import Instrument, Order, OrderItem, Album, Artist, Track, Genre

class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'description']  # Замінили 'instrument_type' на 'type' і видалили 'stock'
    list_filter = ['type']  # Замінили 'instrument_type' на 'type'
    search_fields = ['name', 'description']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'order_date']  # Видалили 'instrument' і 'quantity'
    inlines = [OrderItemInline]  # Додаємо інлайн для OrderItem, щоб показувати інструменти та кількість
    search_fields = ['customer_name', 'customer_email']
    list_filter = ['order_date']

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_date', 'genre']
    list_filter = ['genre', 'release_date']
    search_fields = ['title', 'artist__name']

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'formation_date']
    search_fields = ['name', 'bio']

class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'track_number', 'duration']
    list_filter = ['album']
    search_fields = ['title']

class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']

# Реєструємо моделі з відповідними класами адміністратора
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)  # Простий реєстр без кастомного адмін-класу
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Genre, GenreAdmin)