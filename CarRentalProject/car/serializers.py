from rest_framework import serializers
from car.models import Customer, Car, Reservation,CarDealer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'vehicle_number', 'model', 'seating_capacity', 'rent_per_day']


class AvailableCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'vehicle_number', 'model', 'seating_capacity', 'rent_per_day', 'availability']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'car', 'issue_date', 'return_date']

class CarDealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'mobile', 'area', 'email']


class CarDetailsReservationSerializer(serializers.Serializer):
    car = CarSerializer()
    current_active_bookings = ReservationSerializer(many=True)

class CustomerLoginSerializer(serializers.Serializer):
    class Meta:
        modeel =Customer
        fields=['email','password']
