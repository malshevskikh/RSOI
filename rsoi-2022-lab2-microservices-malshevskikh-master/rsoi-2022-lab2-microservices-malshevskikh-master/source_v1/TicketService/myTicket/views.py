from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .models import TicketModel
from .serializers import TicketSerializer


# Получить информацию о всех билетах пользователя
@api_view(['GET'])
def get_all_tickets_of_user(request):
    user = request.headers['X-User-Name']
    valid_tickets = TicketModel.objects.filter(username = user)
    if valid_tickets is None:
        return JsonResponse({'message': 'No tickets'}, status=status.HTTP_404_NOT_FOUND)
    elif valid_tickets is not None:
        serializer = TicketSerializer(valid_tickets, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


# Получить информацию по конкретному билету пользователя
@api_view(['GET'])
def get_one_tickets_of_user(request, ticketUid):
    user = request.headers['X-User-Name']
    try:
        valid_ticket = TicketModel.objects.get(username=user, ticket_uid = ticketUid)
        serializer = TicketSerializer(valid_ticket)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except:
        return JsonResponse({'message': 'No tickets'}, status=status.HTTP_404_NOT_FOUND)

# Покупка билета
@api_view(['POST'])
def buy_ticket_for_user(request):
    user = request.headers['X-User-Name']
    #print(TicketModel.status.PAID)
    #data = JSONParser().parse(request)
    data = {
        "username": user,
        "flight_number": request.data['flightNumber'],
        "price": request.data['price'],
        "status": TicketModel.StatusOfFlight.PAID
    }

    serializer = TicketSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# Возврат билета
@api_view(['PATCH'])
def delete_ticket(request, ticketUid):
    user = request.headers['X-User-Name']
    try:
        valid_ticket = TicketModel.objects.get(username=user, ticket_uid = ticketUid)
        if valid_ticket.status == "PAID":
            valid_ticket.status = "CANCELED"
            valid_ticket.save()
            return JsonResponse({'message': 'Возврат билета успешно выполнен'}, status=status.HTTP_204_NO_CONTENT, safe=False)
        else:
            return JsonResponse({'message': 'Возврат уже был выполнен'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse({'message': 'Билет не найден'}, status=status.HTTP_404_NOT_FOUND)