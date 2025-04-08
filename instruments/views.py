from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Instrument, Order
from .serializers import InstrumentSerializer, OrderSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# -------- INSTRUMENTS --------

class InstrumentListCreateAPIView(APIView):
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

    @swagger_auto_schema(request_body=InstrumentSerializer, responses={200: InstrumentSerializer, 400: 'Bad Request', 404: 'Not Found'})
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

    @swagger_auto_schema(request_body=OrderSerializer, responses={200: OrderSerializer, 400: 'Bad Request', 404: 'Not Found'})
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
