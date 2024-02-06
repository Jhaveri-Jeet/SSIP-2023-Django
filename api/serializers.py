from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    body = serializers.CharField()
    to = serializers.ListField()
    date= serializers.DateField()
class SMSSerializer(serializers.Serializer):
    HearingDate=serializers.DateField()
    Message=serializers.CharField()
    To=serializers.ListField(required=False)
    