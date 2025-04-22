import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
import os

# Create your views here.

#Запросы по пользваотелю
#Информация о пользователе
@api_view(['GET'])
def gateway_get_user_info(request):
    print('ok')
    list_of_tickets = []
    user = request.headers.get('X-User-Name')
    if user is not None:
        #valid_tickets = requests.get("http://127.0.0.1:8070/api/v1/tickets", headers={"X-User-Name": user })
        valid_tickets = requests.get("http://ticket:8070/api/v1/tickets", headers={"X-User-Name": user})
        #return JsonResponse(valid_tickets.json(), status=valid_tickets.status_code, safe=False)
        print(valid_tickets)
        if valid_tickets.status_code == 200:
            print("vvvvv:", valid_tickets)
            valid_tickets = valid_tickets.json()
            print("aaaaa:", valid_tickets)
            #print(valid_tickets['flight_number'])
            for i in valid_tickets:
                flight_number = i['flight_number']
                #valid_flights = requests.get("http://127.0.0.1:8060/api/v1/flights/{}".format(flight_number))
                valid_flights = requests.get("http://flight:8060/api/v1/flights/{}".format(flight_number))
                if valid_flights.status_code == 200:
                    print("dddd:", valid_flights)
                    valid_flights = valid_flights.json()

                    print("dddd:", valid_flights)
                    print(type(valid_flights))
                    #print(valid_flights.from_airport_id)
                    ticket_uid = i['ticket_uid']
                    flight_number = i['flight_number']
                    from_airport_id = valid_flights['fromAirport']
                    print(from_airport_id)
                    to_airport_id = valid_flights['toAirport']
                    datetime = valid_flights['date']
                    price = valid_flights['price']
                    status_of_fl = i['status']
                    my_flight_dto = {
                        "ticketUid": ticket_uid,
                        "flightNumber": flight_number,
                        "fromAirport": from_airport_id,
                        "toAirport": to_airport_id,
                        "date": datetime,
                        "price": price,
                        "status": status_of_fl
                    }
                    list_of_tickets.append(my_flight_dto)
            #privilege_of_user = requests.get("http://127.0.0.1:8050/api/v1/privilege", headers={"X-User-Name": user})
            privilege_of_user = requests.get("http://bonus:8050/api/v1/privilege", headers={"X-User-Name": user })
            if privilege_of_user.status_code == 200:
                privilege_of_user = privilege_of_user.json()
                balance = privilege_of_user['balance']
                status_of_pr = privilege_of_user['status']
                me_dto = {
                    "tickets": list_of_tickets,
                    "privilege": {
                        "balance": balance,
                        "status": status_of_pr
                    }
                }
                return JsonResponse(me_dto, status=status.HTTP_200_OK, safe=False)
            return JsonResponse(privilege_of_user.json(), status=privilege_of_user.status_code)
        return JsonResponse(valid_tickets.json(), status=valid_tickets.status_code)
    else:
        return JsonResponse({'message': 'user with this name doesnt exist'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

#Запросы для TicketService
#Информация по всем билетам пользователя и покупка билета
@api_view(['GET', 'POST'])
def gateway_get_all_tickets_and_buy(request):
    #print('ok')
    global payment_with_bonus, my_flight_dto
    d = request.data
    list_of_tickets = []
    user = request.headers.get('X-User-Name')
    if user is not None:
        if request.method == 'GET':
            #print('OMG')
            #valid_tickets = requests.get("http://127.0.0.1:8070/api/v1/tickets", headers={"X-User-Name": user})
            valid_tickets = requests.get("http://ticket:8070/api/v1/tickets", headers={"X-User-Name": user})
            if valid_tickets.status_code == 200:
                valid_tickets = valid_tickets.json()
                for i in valid_tickets:
                    flight_number = i['flight_number']
                    #valid_flights = requests.get("http://127.0.0.1:8060/api/v1/flights/{}".format(flight_number))
                    valid_flights = requests.get("http://flight:8060/api/v1/flights/{}".format(flight_number))
                    if valid_flights.status_code == 200:
                        print("dddd:", valid_flights)
                        valid_flights = valid_flights.json()

                        print("dddd:", valid_flights)
                        print(type(valid_flights))
                        # print(valid_flights.from_airport_id)
                        ticket_uid = i['ticket_uid']
                        print(ticket_uid)
                        flight_number = i['flight_number']
                        from_airport_id = valid_flights['fromAirport']
                        print(from_airport_id)
                        to_airport_id = valid_flights['toAirport']
                        datetime = valid_flights['date']
                        price = valid_flights['price']
                        status_of_fl = i['status']
                        my_flight_dto = {
                            "ticketUid": ticket_uid,
                            "flightNumber": flight_number,
                            "fromAirport": from_airport_id,
                            "toAirport": to_airport_id,
                            "date": datetime,
                            "price": price,
                            "status": status_of_fl
                        }
                        list_of_tickets.append(my_flight_dto)
                return JsonResponse(list_of_tickets, status=status.HTTP_200_OK, safe = False)
            else:
                return JsonResponse({'message': 'no tickets for this user'}, status=valid_tickets.status_code, safe=False)
        elif request.method == 'POST':
            #print('OMG')
            #print(request.data['flightNumber'])
            flightNumber = request.data['flightNumber']
            #flight_is_valid = requests.get("http://127.0.0.1:8060/api/v1/flights/{}".format(flightNumber))
            flight_is_valid = requests.get("http://flight:8060/api/v1/flights/{}".format(flightNumber))
            flight = flight_is_valid.json()
            flight_number = flight.get('flightNumber')
            #print("sss:", flight_is_valid.status_code, flight_number, flightNumber)
            print(flight)

            if (flight_is_valid.status_code != 200) or (flightNumber != flight_number):
                return JsonResponse({'message': 'this flight does not exist'}, status=status.HTTP_404_NOT_FOUND, safe=False)

            print("NOT OK!!!")
            #buy_ticket = requests.post("http://127.0.0.1:8070/api/v1/tick", headers={"X-User-Name": user }, data=d)
            buy_ticket = requests.post("http://ticket:8070/api/v1/tick", headers={"X-User-Name": user}, data=d)
            if buy_ticket.status_code != 201:
                return JsonResponse({'message': 'can not pay for this flight'}, status=buy_ticket.status_code, safe=False)
            #print("NOT OK!!!")
            #print("can make ticket!")
            type_of_payment = request.data['paidFromBalance']
            price_data = request.data["price"]
            tick = buy_ticket.json()
            print(tick)
            ticket_uniq = tick.get('ticket_uid')


            data_for_privilege = {
                "ticketUid": ticket_uniq,
                "price": price_data,
                "paidFromBalance": type_of_payment
            }

            print(data_for_privilege)
            #payment_with_bonus = requests.patch("http://127.0.0.1:8050/api/v1/change_count", headers={"X-User-Name": user}, data=data_for_privilege)
            payment_with_bonus = requests.patch("http://bonus:8050/api/v1/change_count", headers={"X-User-Name": user}, data=data_for_privilege)
            if payment_with_bonus.status_code != 200:
                return JsonResponse(payment_with_bonus.json(), status=payment_with_bonus.status_code, safe=False)

            bonus = payment_with_bonus.json()

            print("1:", flight)
            print("2:", tick)
            print("3:", bonus)

            #if type_of_payment == True:
            #    change_flag = 0
            #    payment_with_bonus = requests.patch("http://127.0.0.1:8050/api/v1/change_count/{}".format(change_flag), headers={"X-User-Name": user }, data=data_for_privilege)
            #    if payment_with_bonus.status_code != 200:
            #        return JsonResponse(payment_with_bonus.json(), status=payment_with_bonus.status_code, safe=False)
            #elif type_of_payment == False:
            #    change_flag = 1
            #    payment_without_bonus = requests.patch("http://127.0.0.1:8050/api/v1/change_count/{}".format(change_flag), headers={"X-User-Name": user }, data=data_for_privilege)
            #    if payment_without_bonus.status_code != 200:
            #        return JsonResponse(payment_without_bonus.json(), status=payment_without_bonus.status_code, safe=False)

            flight_number = flight.get('flightNumber')
            from_airport_id = flight.get('fromAirport')
            to_airport_id = flight.get('toAirport')
            datetime = flight.get('date')
            price = request.data['price']
            status_of_fl = tick.get('status')
            paid_by_m =bonus.get('paidByMoney')
            paid_by_b = bonus.get('paidByBonuses')

            if 'Message' in bonus:

                print("сюда")
                m = bonus.get('Message')
                my_flight_dto = {
                    "ticketUid": ticket_uniq,
                    "flightNumber": flight_number,
                    "fromAirport": from_airport_id,
                    "toAirport": to_airport_id,
                    "date": datetime,
                    "price": price,
                    "paidByMoney": paid_by_m,
                    "paidByBonuses": paid_by_b,
                    "status": status_of_fl,
                    "privilege": {
                        "message": m
                    }
                }

            elif 'privilege' in bonus:

                print(" не сюда")
                p = bonus.get('privilege')
                my_flight_dto = {
                    "ticketUid": ticket_uniq,
                    "flightNumber": flight_number,
                    "fromAirport": from_airport_id,
                    "toAirport": to_airport_id,
                    "date": datetime,
                    "price": price,
                    "paidByMoney": paid_by_m,
                    "paidByBonuses": paid_by_b,
                    "status": status_of_fl,
                    "privilege": p
                }

            #my_flight_dto.update(flight_is_valid.json())
            #my_flight_dto.update(buy_ticket.json())
            #my_flight_dto.update(payment_with_bonus.json())


            return JsonResponse(my_flight_dto, status=status.HTTP_200_OK, safe=False)
    else:
        return JsonResponse({'message': 'user with this name doesnt exist'}, status=status.HTTP_400_BAD_REQUEST, safe=False)


#Информация по конкретному билету и возврат билета
@api_view(['GET', 'DELETE'])
def gateway_get_ticket_info_and_cancel(request, ticketUid):
    print('ok')
    user = request.headers.get('X-User-Name')
    if user is not None:
        if request.method == 'GET':
            print("hhhhh")
            #valid_ticket = requests.get("http://127.0.0.1:8070/api/v1/tickets/{}".format(ticketUid), headers={"X-User-Name": user})
            valid_ticket = requests.get("http://ticket:8070/api/v1/tickets/{}".format(ticketUid), headers={"X-User-Name": user})
            if valid_ticket.status_code == 200:
                #print("vvvvv:", valid_ticket)
                valid_ticket = valid_ticket.json()
                print(valid_ticket)
                flight_number = valid_ticket['flight_number']
                #valid_flights = requests.get("http://127.0.0.1:8060/api/v1/flights/{}".format(flight_number))
                valid_flights = requests.get("http://flight:8060/api/v1/flights/{}".format(flight_number))
                if valid_flights.status_code == 200:
                    print("dddd:", valid_flights)
                    valid_flights = valid_flights.json()

                    print("dddd:", valid_flights)
                    print(type(valid_flights))
                    #print(valid_flights.from_airport_id)
                    ticket_uid = valid_ticket['ticket_uid']
                    print(ticket_uid)
                    flight_number = valid_ticket['flight_number']
                    from_airport_id = valid_flights['fromAirport']
                    print(from_airport_id)
                    to_airport_id = valid_flights['toAirport']
                    datetime = valid_flights['date']
                    price = valid_flights['price']
                    status_of_fl = valid_ticket['status']
                    my_flight_dto = {
                        "ticketUid": ticket_uid,
                        "flightNumber": flight_number,
                        "fromAirport": from_airport_id,
                        "toAirport": to_airport_id,
                        "date": datetime,
                        "price": price,
                        "status": status_of_fl
                    }
                    print(my_flight_dto)
                    return JsonResponse(my_flight_dto, status=status.HTTP_200_OK, safe=False)
                else:
                    return JsonResponse({'message': 'no flights for this number'}, status=valid_flights.status_code, safe=False)
            else:
                return JsonResponse({'message': 'no tickets for this user'}, status=valid_ticket.status_code, safe=False)
        elif request.method == 'DELETE':
            #change_ticket = requests.patch("http://127.0.0.1:8070/api/v1/del_tick/{}".format(ticketUid), headers={"X-User-Name": user})
            change_ticket = requests.patch("http://ticket:8070/api/v1/del_tick/{}".format(ticketUid), headers={"X-User-Name": user})
            if change_ticket.status_code != 204:
                return JsonResponse({'message': 'Билет либо не найден, либо уже отменен'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
            #return_money = requests.patch("http://127.0.0.1:8050/api/v1/return_money/{}".format(ticketUid), headers={"X-User-Name": user})
            return_money = requests.patch("http://bonus:8050/api/v1/return_money/{}".format(ticketUid), headers={"X-User-Name": user})
            if return_money.status_code != 200:
                return JsonResponse({'message': 'Билет отмненен, но не смогли забрать/вренуть бонусы, возможно у вас нет бонусного счета'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
            return JsonResponse({'message': 'Возврат билета успешно выполнен'}, status=status.HTTP_204_NO_CONTENT, safe=False)
    else:
        return JsonResponse({'message': 'user with this name doesnt exist'}, status=status.HTTP_400_BAD_REQUEST, safe=False)



#Запросы для FlightService
#Получить список рейстов
@api_view(['GET'])
def gateway_get_all_flights(request):
    page = request.GET.get('page')
    size = request.GET.get('size')
    if (page is not None) and (size is not None):
        #list_of_flight = requests.get("http://127.0.0.1:8060/api/v1/flights?page={}&size={}".format(page, size))
        list_of_flight = requests.get("http://flight:8060/api/v1/flights?page={}&size={}".format(page, size))
        return JsonResponse(list_of_flight.json(), status=list_of_flight.status_code, safe=False)
    else:
        #list_of_flight = requests.get("http://127.0.0.1:8060/api/v1/flights")
        list_of_flight = requests.get("http://flight:8060/api/v1/flights")
        return JsonResponse(list_of_flight.json(), status=list_of_flight.status_code, safe=False)


#Запросы для BonusService
#Получить информацию о состоянии бонусного счета
@api_view(['GET'])
def gateway_get_privilege_info(request):
    user = request.headers.get('X-User-Name')
    if user is not None:
        #privilege_of_user = requests.get("http://127.0.0.1:8050/api/v1/privilege_history", headers={"X-User-Name": user})
        privilege_of_user = requests.get("http://bonus:8050/api/v1/privilege_history", headers={"X-User-Name": user})
        return JsonResponse(privilege_of_user.json(), status=privilege_of_user.status_code, safe=False)
    else:
        return JsonResponse({'message': 'user with this name doesnt exist'}, status=status.HTTP_400_BAD_REQUEST, safe=False)