from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Album, Artist, Track, Genre, Instrument, Order
from .serializers import (
    AlbumSerializer,
    ArtistSerializer,
    TrackSerializer,
    GenreSerializer,
    InstrumentSerializer,  # Додали імпорт
    OrderSerializer
)
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# -------- INSTRUMENTS --------

class InstrumentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: InstrumentSerializer(many=True)})
    def get(self, request):
        instruments = Instrument.objects.all()
        serializer = InstrumentSerializer(instruments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=InstrumentSerializer, responses={201: InstrumentSerializer})
    def post(self, request):
        serializer = InstrumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstrumentDetailAPIView(APIView):
    @swagger_auto_schema(responses={200: InstrumentSerializer, 404: 'Not Found'})
    def get(self, request, pk):
        try:
            instrument = Instrument.objects.get(pk=pk)
            serializer = InstrumentSerializer(instrument)
            return Response(serializer.data)
        except Instrument.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=InstrumentSerializer,
                         responses={200: InstrumentSerializer, 400: 'Bad Request', 404: 'Not Found'})
    def put(self, request, pk):
        try:
            instrument = Instrument.objects.get(pk=pk)
            serializer = InstrumentSerializer(instrument, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Instrument.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(responses={204: 'No Content', 404: 'Not Found'})
    def delete(self, request, pk):
        try:
            instrument = Instrument.objects.get(pk=pk)
            instrument.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Instrument.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# -------- ORDERS --------

class OrderListCreateAPIView(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=OrderSerializer, responses={201: OrderSerializer})
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer, 404: 'Not Found'})
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=OrderSerializer,
                         responses={200: OrderSerializer, 400: 'Bad Request', 404: 'Not Found'})
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(responses={204: 'No Content', 404: 'Not Found'})
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# -------- ALBUMS --------

class AlbumListView(APIView):
    permission_classes = [IsAuthenticated]  # вимагає аутентифікації

    @swagger_auto_schema(
        operation_description="Отримати список всіх альбомів",
        responses={200: AlbumSerializer(many=True)}
    )
    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Створити новий альбом",
        request_body=AlbumSerializer,
        responses={201: AlbumSerializer}
    )
    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetailView(APIView):
    permission_classes = [IsAuthenticated]  # вимагає аутентифікації

    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Отримати альбом за ID",
        responses={200: AlbumSerializer, 404: "Альбом не знайдено"}
    )
    def get(self, request, pk):
        album = self.get_object(pk)
        if album is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Оновити альбом за ID",
        request_body=AlbumSerializer,
        responses={200: AlbumSerializer, 400: "Неправильні дані", 404: "Альбом не знайдено"}
    )
    def put(self, request, pk):
        album = self.get_object(pk)
        if album is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Видалити альбом за ID",
        responses={204: "Альбом видалено", 404: "Альбом не знайдено"}
    )
    def delete(self, request, pk):
        album = self.get_object(pk)
        if album is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------- ADMIN ONLY VIEW --------

class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_description="Ендпоінт доступний тільки для адміністраторів",
        responses={200: "Повідомлення для адміна", 403: "Доступ заборонено"}
    )
    def get(self, request):
        return Response({"message": "You are an admin!"})
