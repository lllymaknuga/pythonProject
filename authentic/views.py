from datetime import timedelta
from random import randint

from django.shortcuts import render
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from users.models import OtpToken, CustomUser
from users.serializres import PhoneRegistrationSerializer, PhoneValidatorSerializer

from smsru.service import SmsRuApi


class Registration(APIView):
    serializer_class = PhoneRegistrationSerializer

    def post(self, request):
        ser = self.serializer_class(
            data=request.data
        )
        if ser.is_valid():

            otp_code = randint(1000, 10000)
            # list_otp_code = OtpToken.objects.filter() # Все токены, кот-ые были до нового is_active = True сделать False
            # Пишу if, кот-й
            print(otp_code)
            attempts_list = OtpToken.objects.filter(data_send__day=timezone.now().day,
                                                    phone=ser.validated_data['phone']).count()
            if OtpToken.objects.filter(phone=ser.validated_data['phone']).count() != 0:
                if attempts_list >= 5:
                    return Response('Attempts not ', status=status.HTTP_403_FORBIDDEN)
            OtpToken.objects.create(phone=ser.validated_data['phone'], otp_code=otp_code)
            api = SmsRuApi()
            api.send_one_sms(ser.validated_data['phone'], f'Ваш код для подвтерждения регистрации {otp_code}')
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Validate(APIView):
    serializer_class = PhoneValidatorSerializer

    def post(self, request):
        ser = self.serializer_class(
            data=request.data
        )
        if ser.is_valid():
            phone = ser.validated_data.get('phone')
            otp_code = ser.validated_data.get('otp_code')
            otp_code_object = OtpToken.objects.filter(otp_code=otp_code, phone=phone).last()
            # last_getting_token = OtpToken.objects.filter(phone=ser.validated_data['phone']).last()
            if otp_code_object is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            if timezone.now() - otp_code_object.data_send > timedelta(minutes=3):
                return Response('Expired', status=status.HTTP_403_FORBIDDEN)
            # phone=phone, defaults=username
            user, _ = CustomUser.objects.get_or_create(phone=phone, username=ser.validated_data['username'])
            token, have_token = Token.objects.get_or_create(user=user)
            if not have_token:
                token = Token.objects.filter(user=user).last().update()
            return Response(f'{token}', status=status.HTTP_200_OK)
