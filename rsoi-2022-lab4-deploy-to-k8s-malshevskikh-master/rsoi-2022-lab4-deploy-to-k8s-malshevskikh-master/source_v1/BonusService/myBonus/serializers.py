from rest_framework import serializers
from .models import PrivilegeModel, PrivilegeHistoryModel

class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivilegeModel
        fields = ['id', 'username', 'status', 'balance']

class PrivilegeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivilegeHistoryModel
        fields = ['id', 'privilege_id', 'ticket_uid', 'datetime', 'balance_diff', 'operation_type']

