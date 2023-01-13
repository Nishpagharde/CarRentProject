from car import views
from django.urls import path

urlpatterns = [
    path('', views.home),

    path('customer/', views.view_all_customers),
    path('customer/add/', views.add_customer),
    path('customer/<int:cust_pk>/', views.view_customer_details),
    path('customer/<int:cust_pk>/update/', views.edit_customer_details),
    path('customer/<int:cust_pk>/delete/', views.delete_customer),

    path('car/', views.view_all_cars),
    path('car/add/', views.add_car), # API 1: Add new cars
    path('car/<int:car_pk>/', views.view_car_details),
    path('car/<int:car_pk>/active_booking/', views.view_car_details_active_booking), # API 3: Show details of car with booking details
    path('car/<int:car_pk>/update/', views.edit_car_details),
    path('car/<int:car_pk>/delete/', views.delete_car),

    path('rent/', views.view_all_reservations),
    path('rent/book/', views.book_car), # API 2: Book an available car
    path('rent/<int:rent_pk>/',views.view_reservation_details),
    path('rent/<int:rent_pk>/extend/', views.extend_reservation_date), # API 5: Extend date of reservation.
    path('rent/<int:rent_pk>/cancel/', views.cancel_reservation), # API 6: Cancel Specific booking

    path('car/status/', views.view_all_cars_on_given_date) ,# API 4: Show cars with availability status on given date.
    path('dealer/', views.view_all_dealer),
    path('dealer/add/',views. add_dealer),
    path('dealer/<int:deal_pk>/',views.view_dealer_details),
    path('dealer/<int:deal_pk>/update/',views.edit_dealer_details),
    path('dealer/<int:dealer_pk>/delete/',views.delete_dealer),
    path('login/',views.CustomerLogin),

]