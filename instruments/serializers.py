from rest_framework import serializers
from .models import Album, Artist, Track, Genre, Instrument, Order


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'formation_date']

    def validate_name(self, value):
        # Перевірка, що ім'я артиста не містить цифр
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Artist name should not contain numbers.")
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

    def validate_release_date(self, value):
        # Перевірка, що дата релізу не в майбутньому
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Release date cannot be in the future.")
        return value

    def validate(self, data):
        # Комплексна валідація
        if 'title' in data and 'artist' in data:
            if data['title'].lower() == 'unknown' and data['artist'] is None:
                raise serializers.ValidationError("Cannot have 'unknown' title with no artist specified.")
        return data


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'


# Додаємо новий серіалізатор для Instrument
class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'