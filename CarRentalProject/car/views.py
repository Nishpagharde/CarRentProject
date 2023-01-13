from collections import namedtuple
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime, date
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from car.models import  Car, Reservation,Customer,CarDealer
from car.serializers import (CarSerializer, ReservationSerializer, CarDetailsReservationSerializer,
                             AvailableCarSerializer,CustomerSerializer, CarDealerSerializer,CustomerLoginSerializer)
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
@api_view(['GET'])
def home(request):
    """
    API endpoint for home page.
    """
    if request.method == 'GET':
        data = [{'message': 'Welcome to Car-Rental-Agency'}]
        return JsonResponse(data, safe=False)


@api_view(['GET'])
def view_all_cars(request):
    """
    API endpoint for displaying all car details.
    """
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_car_details(request, car_pk):
    """
    API endpoint for displaying particular car details.
    """
    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return Response(serializer.data)


@api_view(['GET'])
def view_car_details_active_booking(request, car_pk):
    """
    API endpoint for displaying specific car details with
    its current active reservation details.
    """
    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        current_date = date.today()
        CarBookingDetails = namedtuple('CarBookingDetails', ('car', 'current_active_bookings'))

        # Conditions for filtering only currently active bookings of a particular car
        # suffix "__gte" stands for Greater Than or Equal to.
        condition_1 = Q(issue_date__gte=current_date)
        condition_2 = Q(return_date__gte=current_date)

        carBookingDetails = CarBookingDetails(
            car=car,
            current_active_bookings=Reservation.objects.filter(car=car_pk).filter(condition_1 | condition_2),
        )
        serializer = CarDetailsReservationSerializer(carBookingDetails)
        return Response(serializer.data)


@api_view(['POST'])
def add_car(request):
    """
    API endpoint for adding new car to the system,
    which could be used for renting.
    """
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_car_details(request, car_pk):
    """
    API endpoint for editing a particular car details.
    """
    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CarSerializer(car, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_car(request, car_pk):
    """
    API endpoint for deleting car from the system.
    """
    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@parser_classes([JSONParser])
def view_all_cars_on_given_date(request):
    """
    API endpoint for showing the cars with their availability status on a given date.
    And filter the cars based on various fields.
    """
    if request.method == 'GET':
        # Fetch date from url if passed or else set default to today's date.
        date_to_check = request.GET.get('date', str(date.today()))
        date_to_check = datetime.strptime(date_to_check, '%Y-%m-%d').date()  # Convert date to datetime format.

        # Fetch filters like model, capacity or availability status
        # if passed any as GET request URL parameters
        model = request.GET.get('model')
        capacity = request.GET.get('capacity')
        availability = request.GET.get('availability')

        # Filter all car reservations which falls in between date_to_check
        condition_1 = Q(issue_date__gte=date_to_check)
        condition_2 = Q(return_date__gte=date_to_check)
        reservations = Reservation.objects.filter(condition_1 | condition_2)
        serializer = ReservationSerializer(reservations, many=True)
        reservation_data = serializer.data

        # Get list of car ids which are reserved on the given date.
        occupied_car_id_lists = []
        for i in range(len(reservation_data)):
            occupied_car_id_lists.append(reservation_data[i]['car'])
        list_of_car_id = list(set(occupied_car_id_lists))

        # Setting availability of all car to True
        Car.objects.all().update(availability=True)

        # Setting availability of all reserved car to False
        for car_id in list_of_car_id:
            Car.objects.filter(id=car_id).update(availability=False)

        # Querying and filtering the cars based on various fields.
        cars = Car.objects.all()
        filters = {'model': model, 'seating_capacity': capacity, 'availability': availability}
        for key, value in filters.items():
            if value is not None:
                cars = cars.filter(**{key: value})
        car_serializer = AvailableCarSerializer(cars, many=True)

        return Response(car_serializer.data)

@api_view(['GET'])
def view_all_customers(request):
    """
    API endpoint to show all customer details.
    """
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_customer_details(request, cust_pk):
    """
    API endpoint to show a specific customer details.
    """
    try:
        customer = Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


@api_view(['POST'])
def add_customer(request):
    """
    API endpoint to add customer.
    """
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_customer_details(request, cust_pk):
    """
    API endpint to edit a specific customer details.
    """
    try:
        customer = Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_customer(request, cust_pk):
    """
    API endpoint for deleting customer details.
    """
    try:
        customer = Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def view_all_reservations(request):
    """
    API endpoint for showing all reservations in the system.
    """
    if request.method == 'GET':
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_reservation_details(request, rent_pk):
    """
    API endpoint for showing a particular reservation details.
    """
    try:
        reservation = Reservation.objects.get(pk=rent_pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)


@api_view(['POST'])
def book_car(request):
    """
    API endpoint for booking an available car.
    """
    if request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            current_date = date.today()
            issue_date = serializer.validated_data['issue_date']
            return_date = serializer.validated_data['return_date']

            car = serializer.validated_data['car']
            reservations = Reservation.objects.all().filter(car=car.id)

            # Check if the issue_date of new reservation doesn't clash with any previous reservations
            for r in reservations:
                if r.issue_date <= issue_date <= r.return_date:
                    content = {"message": "The selected car is not available on this date"}
                    return Response(data=json.dumps(content), status=status.HTTP_400_BAD_REQUEST)

            # Check whether issue_date is not older than today's date, and is less equal to return_date
            if current_date <= issue_date and issue_date <= return_date:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def extend_reservation_date(request, rent_pk):
    """
    API endpoint for extending the booking of the car,
    if the car is not already reserved for the dates
    user wants to extend the booking.
    """
    try:
        reservation = Reservation.objects.get(pk=rent_pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ReservationSerializer(reservation, data=request.data)

        if serializer.is_valid():
            current_date = date.today()
            issue_date = serializer.validated_data['issue_date']
            return_date = serializer.validated_data['return_date']

            car = serializer.validated_data['car']
            reservations = Reservation.objects.all().filter(car=car.id)

            # Check if the return_date of new reservation doesn't clash with any previous reservations
            for r in reservations:
                if r.issue_date <= return_date <= r.return_date:
                    res = {"message": "Failed to extend the date. Car is not available."}
                    return Response(data= json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

            # Check whether issue_date is not older than today's date, and is less equal to return_date
            if current_date <= issue_date and issue_date <= return_date:
                serializer.save()
                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def cancel_reservation(request, rent_pk):
    """
    API endpoint for cancelling a specific Booking.
    """
    try:
        reservation = Reservation.objects.get(pk=rent_pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def view_all_dealer(request):
    """
    API endpoint to show all customer details.
    """
    if request.method == 'GET':
        dealer = CarDealer.objects.all()
        serializer =  CarDealerSerializer(dealer, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_dealer_details(request, deal_pk):
    """
    API endpoint to show a specific customer details.
    """
    try:
        dealer =  CarDealer.objects.get(pk=deal_pk)
    except  CarDealer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer =  CarDealerSerializer((dealer))
        return Response(serializer.data)


@api_view(['POST'])
def add_dealer(request):
    """
    API endpoint to add customer.
    """
    if request.method == 'POST':
        serializer =  CarDealerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_dealer_details(request, deal_pk):
    """
    API endpint to edit a specific customer details.
    """
    try:
        dealer =  CarDealer.objects.get(pk=deal_pk)
    except  CarDealer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer =  CarDealerSerializer(dealer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_dealer(request, deal_pk):
    """
    API endpoint for deleting customer details.
    """
    try:
        dealer =  CarDealer.objects.get(pk=deal_pk)
    except  CarDealer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        dealer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def CustomerLogin(self,request,format=None):
        serializer=CustomerLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password = serializer.data.get('password')
            customer=authenticate(email=email,password=password)
            if customer is not None:
                return Response({'msg':'Login success'},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors': {'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)