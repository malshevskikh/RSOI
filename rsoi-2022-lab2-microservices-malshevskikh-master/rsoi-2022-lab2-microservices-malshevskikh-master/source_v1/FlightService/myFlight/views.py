import json

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from .models import FlightModel, AirportModel
from .serializers import FlightSerializer, AirportSerializer
from rest_framework import pagination
from dataclasses import dataclass

# Create your views here.

#Создание DTO для полетов
@dataclass
class FlightDto:
    flight_number: str
    datetime: str
    from_airport_id: str
    to_airport_id: str
    price: []

#Создание DTO для полетов со страницами
@dataclass
class FlightPageDto:
    page_of_fl: int
    pageSise: int
    totalElements: int
    items: str

#Получить информацию о полете по его номеру
@api_view(['GET'])
def get_one_flight(request, flight_num):
    try:
        valid_flight = FlightModel.objects.get(flight_number = flight_num)

        #serializer_fl = FlightSerializer(valid_flight)

        air_fr = valid_flight.from_airport_id.id
        air_to = valid_flight.to_airport_id.id

        valid_air_fr = AirportModel.objects.get(id = air_fr)
        valid_air_to = AirportModel.objects.get(id = air_to)

        serializer_air_fr = ""
        serializer_air_to = ""

        serializer_air_fr = valid_air_fr.city + " " + valid_air_fr.name
        serializer_air_to = valid_air_to.city + " " + valid_air_to.name

        #serializer_air_fr = valid_air_fr.name + ", " + valid_air_fr.city
        #serializer_air_to = valid_air_to.name + ", " + valid_air_to.city

        flight_dto = FlightDto(
            flight_number = valid_flight.flight_number,
            datetime = str(valid_flight.datetime),
            from_airport_id = serializer_air_fr,
            to_airport_id = serializer_air_to,
            price = valid_flight.price,
        )

        flight_dto_sec = {
            'flightNumber': valid_flight.flight_number,
            'fromAirport': serializer_air_fr,
            'toAirport': serializer_air_to,
            'date': str(valid_flight.datetime),
            'price': valid_flight.price,
        }

        json_flight_dto = json.dumps(flight_dto.__dict__)

        return JsonResponse(flight_dto_sec, status=status.HTTP_200_OK, safe=False)
    except:
        return JsonResponse( status=status.HTTP_404_NOT_FOUND)


#Получить список всех полетов
@api_view(['GET'])
def get_list_of_flights(request):
    page = request.GET.get('page')
    size = request.GET.get('size')
    #flights_of_one_page = {}
    flights_of_one_page = []
    print(page)
    print(size)

    print(int(size))
    print((int(page) - 1))
    if (page is not None) and (size is not None):
        startIndex = int(size) * (int(page) - 1)
        endIndex = (int(size) * int(page)) - 1
        print(startIndex)
        print(endIndex)
        if startIndex < 0 or endIndex < 0:
            startIndex = 0
            endIndex = 1
            page = 1
        valid_flights = FlightModel.objects.all()[startIndex:endIndex]
    else:
        valid_flights = FlightModel.objects.all()

    count_of_flights = valid_flights.count()

    for i in valid_flights:
        #посик названия аеропорта, города и старны
        air_fr = i.from_airport_id.id
        air_to = i.to_airport_id.id

        valid_air_fr = AirportModel.objects.get(id = air_fr)
        valid_air_to = AirportModel.objects.get(id = air_to)

        serializer_air_fr = ""
        serializer_air_to = ""


        serializer_air_fr = valid_air_fr.city + " " + valid_air_fr.name
        serializer_air_to = valid_air_to.city + " " + valid_air_to.name

        #serializer_air_fr = valid_air_fr.name + ", " + valid_air_fr.city
        #serializer_air_to = valid_air_to.name + ", " + valid_air_to.city

        flight_dto = {
            "flightNumber": i.flight_number,
            "fromAirport": serializer_air_fr,
            "toAirport": serializer_air_to,
            "date": str(i.datetime),
            "price": i.price
        }

        #flight_dto = FlightDto(
        #    flight_number = i.flight_number,
        #    datetime = str(i.datetime),
        #    from_airport_id = serializer_air_fr,
        #    to_airport_id = serializer_air_to,
        #    price = i.price,
        #)

        #json_flight_dto = json.dumps(flight_dto.__dict__)
        #print(json_flight_dto)

        #flights_of_one_page |= json_flight_dto
        flights_of_one_page.append(flight_dto)

        print(flights_of_one_page)

    flight_page_dto = {
        "page": int(page),
        "pageSize": int(size),
        "totalElements": count_of_flights,
        "items": flights_of_one_page
    }


    #flight_page_dto = FlightPageDto(
    #    page_of_fl = page,
    #    pageSise = size,
    #    totalElements= count_of_flights,
    #    items = flights_of_one_page,
    #)

    #print(flight_page_dto)

    #json_flight_page_dto = json.dumps(flight_page_dto.__dict__)

    #print(json_flight_page_dto)

    return JsonResponse(flight_page_dto, status=status.HTTP_200_OK, safe=False)
