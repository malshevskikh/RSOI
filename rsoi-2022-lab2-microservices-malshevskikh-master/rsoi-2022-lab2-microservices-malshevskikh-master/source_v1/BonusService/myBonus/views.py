import json
import datetime
import uuid
from dataclasses import dataclass
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from .models import PrivilegeModel, PrivilegeHistoryModel
from .serializers import PrivilegeSerializer, PrivilegeHistorySerializer

# Create your views here.
#Создание DTO для истории бонусного счета
@dataclass
class PrivilegeHistoryDto:
    date: str
    balanceDiff: str
    ticketUid: str
    operation_type: str

@dataclass
class PrivilegeDto:
    balance: str
    status: str
    history: []

def adding_info_to_history(privilege_id, ticket_uid, balance_diff, operation_type):
    f = False
    now = datetime.datetime.now()
    print(type(ticket_uid))
    #t = uuid.UUID(ticket_uid)
    #print(type(ticket_uid))
    #print(type(t))
    history_of_transactions = {
        "privilege_id": privilege_id,
        "ticket_uid": ticket_uid,
        "datetime": now,
        "balance_diff": balance_diff,
        "operation_type": operation_type
    }
    print(history_of_transactions)
    serializer = PrivilegeHistorySerializer(data=history_of_transactions)
    #print(serializer.data['ticket_uid'])
    if serializer.is_valid():
        #print(serializer.data['id'])
        serializer.save()
        print(serializer.data['id'])
        print(serializer.data['ticket_uid'])
        print(serializer.data['balance_diff'])
        print(serializer.data['operation_type'])
        f = True
        print(f)
        return JsonResponse({'message': 'добавлено в историю'}, status=status.HTTP_201_CREATED, safe=False), f
    else:
        return JsonResponse({'message': 'не добавлено в историю'}, status=status.HTTP_400_BAD_REQUEST), f

#Получить информацию о бонусном счете одного пользователя
@api_view(['GET'])
def get_userinfo_about_bonus(request):
    user = request.headers['X-User-Name']
    try:
        privilege_list = PrivilegeModel.objects.get(username = user)
        serializer = PrivilegeSerializer(privilege_list)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)


#Получить информацию о бонусном счете одного пользователя, вместе с историей
def get_userinfo_about_history(request):
    user = request.headers['X-User-Name']
    print(user)
    prv_hist = []
    try:
        privilege = PrivilegeModel.objects.get(username=user)
        prv_history = privilege.privilegehistorymodel_set.all()
        #print(prv_history)
        for i in prv_history:

            privilege_history_Dto = {
                "date": i.datetime,
                "ticketUid": i.ticket_uid,
                "balanceDiff": i.balance_diff,
                "operation_type": i.operation_type,
            }
            prv_hist.append(privilege_history_Dto)

        privilege_dto = {
            "balance": privilege.balance,
            "status": privilege.status,
            "history": prv_hist
        }
        #privilege_dto = PrivilegeDto(
        #    balance = privilege.balance,
        #    status = privilege.status,
        #    history = prv_hist
        #)

        #print(privilege_dto)

        return JsonResponse(privilege_dto, status=status.HTTP_200_OK, safe=False)
    except:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def change_privilege_count(request):
    global paid_by_money, paidByBonuses, balanceDiff, oper
    user = request.headers['X-User-Name']
    data = request.data
    print(user)
    print(data)
    #try:
    if user is not None:
        print('fffff:')
        privilege_list = PrivilegeModel.objects.filter(username=user)
        if privilege_list.exists():
            privilege_list = PrivilegeModel.objects.get(username=user)
            print('fffff:', privilege_list)
            prc = request.data['price']
            prc = int(prc)
            type_of_payment = request.data['paidFromBalance']
            print(type_of_payment, type(type_of_payment))
            if type_of_payment == 'True':
                #print("Надо вызвать PATCH для PrivilegeService со списанием бонусов")
                print(data)
                if prc < privilege_list.balance:
                    paid_by_money = 0
                    paidByBonuses = prc
                    balanceDiff = prc
                    privilege_list.balance = privilege_list.balance - prc

                elif prc >= privilege_list.balance:
                    paid_by_money = prc - privilege_list
                    paidByBonuses = privilege_list.balance
                    balanceDiff = privilege_list.balance
                    privilege_list.balance = 0
                privilege_list.save()
                print("dddddd")
                oper = PrivilegeHistoryModel.OperationType.DEBIT_THE_ACCOUNT
                print("[[[[[[[")
            elif type_of_payment == 'False':
                #print("Надо вызвать PATCH для PrivilegeService без списания бонусов")
                #print(data)
                print('22222222')
                paid_by_money = prc
                paidByBonuses = 0
                balanceDiff = prc / 10
                privilege_list.balance = privilege_list.balance + balanceDiff
                privilege_list.save()
                oper = PrivilegeHistoryModel.OperationType.FILL_IN_BALANCE
                #print("money:", paid_by_money)
            balance_data = {
                "paidByMoney": paid_by_money,
                "paidByBonuses": paidByBonuses,
                "privilege": {
                    "balance": privilege_list.balance,
                    "status": privilege_list.status
                }
            }

            print("Тикет:", request.data['ticketUid'])
            #Добавление в историю
            adding_info_to_history(privilege_list.id, request.data['ticketUid'], balanceDiff, oper)
            return JsonResponse(balance_data, status=status.HTTP_200_OK, safe = False)
        else:
            prc = request.data['price']
            prc = int(prc)
            balance_data = {
                "paidByMoney": prc,
                "paidByBonuses": 0,
                "Message": 'Пользователя нет в системе лояльности'
            }
            return JsonResponse(balance_data, status=status.HTTP_200_OK, safe=False)
    #except:
    else:
        return JsonResponse({'message': 'не имзменен баланс'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['PATCH'])
def return_privilege_count(request, ticket_id):
    print("AGAIN!!!")
    user = request.headers['X-User-Name']
    if user is not None:
        print("вернуть бонусы или отдть деньги")
        user_privilege_info = PrivilegeModel.objects.get(username=user)
        id_of_user = user_privilege_info.id
        history_of_user = PrivilegeHistoryModel.objects.get(privilege_id=id_of_user, ticket_uid=ticket_id)
        print("История:", history_of_user)
        print(history_of_user.balance_diff)
        oper = history_of_user.operation_type

        if oper == PrivilegeHistoryModel.OperationType.FILL_IN_BALANCE:
            print("1")
            user_privilege_info.balance = user_privilege_info.balance - history_of_user.balance_diff
            if user_privilege_info.balance < 0:
                user_privilege_info.balance = 0
        elif oper == PrivilegeHistoryModel.OperationType.DEBIT_THE_ACCOUNT:
            print("2")
            user_privilege_info.balance = user_privilege_info.balance + history_of_user.balance_diff
        user_privilege_info.save()
        adding_info_to_history(id_of_user, ticket_id, history_of_user.balance_diff, oper)
        return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
    else:
        print("rermfcm")
        return JsonResponse({'message': 'пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST, safe=False)