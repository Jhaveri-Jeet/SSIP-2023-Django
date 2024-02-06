from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .serializers import *
from ssip_api.settings import EMAIL_HOST_USER
from rest_framework.permissions import AllowAny

from threading import Thread
from datetime import timedelta
from django.utils import timezone

from twilio.rest import Client

account_sid = 'ACf89a17bfe967b685c8660dd5e431189f'
auth_token = '073969794a21bdf7be68ab22a346b8f9'
client = Client(account_sid, auth_token)



class SentSMSView(APIView):
    permission_classes=[AllowAny]
    @staticmethod
    def sendSms(body,to):
        message = client.messages.create(
        from_='+14155824031',
        body=f'{body}',
        # to=f"+91{to}"
        to ='+919712791515'
        )
        message.date_sent()
    def post(self, request, *args, **kwargs):
        serializer = SMSSerializer(data=request.data)

        if serializer.is_valid():
            HearingDate = serializer.validated_data['HearingDate']
            Message = serializer.validated_data['Message']
            To = serializer.validated_data.get('To')

            try:
                # Set the time for 24 hours before the specified HearingDate
                scheduled_time = HearingDate - timedelta(days=1)

                # If the scheduled time is in the future, schedule the SMS
                if scheduled_time == timezone.now().date():

                    # Calculate the time difference between now and the scheduled time
                    time_difference = scheduled_time - timezone.now().date()

                    # Calculate the time to sleep in seconds
                    time_to_sleep = time_difference.total_seconds()

                    # Create a thread to send the SMS
                    thread = Thread(target=self.sendSms, args=(Message, To))
                    thread.daemon = True
                    thread.start()

                    return Response({'success': f'SMS will be sent 24 hours before the specified date ({scheduled_time}).'},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'HearingDate has already passed.'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailView(APIView):
    permission_classes=[AllowAny]
    @staticmethod
    def sendHearingmail(subject, body,to:list):
        print("Sending haearingmail")
        for to_email in to:
                    send_mail(subject, body, EMAIL_HOST_USER, [to_email])
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            date = serializer.validated_data['date']

            subject = serializer.validated_data['subject']
            body = serializer.validated_data['body']
        
            to = serializer.validated_data.get('to', [])
            print(subject, body, to)
            try:

                scheduled_time = date - timedelta(days=1)
                print(scheduled_time)
                print(timezone.now().date())
                # print(scheduled_time <= timezone.now().date(),scheduled_time) 
                # If the scheduled time is in the future, schedule the SMS
                if scheduled_time == timezone.now().date():
                    # Calculate the time difference between now and the scheduled time
                    time_difference = scheduled_time - timezone.now().date()

                    # Calculate the time to sleep in seconds
                    time_to_sleep = time_difference.total_seconds()

                    # Create a thread to send the SMS
                    thread = Thread(target=self.sendHearingmail, args=(subject,body,to))
                    thread.daemon = True
                    thread.start()
  
                    return Response({'success': f'Email will be sent 24 hours before the specified date ({scheduled_time}).'},
                                    status=status.HTTP_200_OK)
                
                return Response({'success': 'Email will be sent 24 hours '}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)