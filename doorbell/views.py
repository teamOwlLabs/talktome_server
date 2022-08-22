from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from firebase_admin import messaging

from doorbell.serializers import (
    VisitSerializer,
    CategorySerializer,
    ClientTokenSerializer,
)
from doorbell.models import Category, ClientToken

def send_to_firebase_cloud_messaging(title_msg, body_msg):
    # Client SDK Token
    registration_token = ClientToken.objects.first().fcm_token

    # TODO: Set Default Message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title_msg,
            body=body_msg,
        ),
        token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


@csrf_exempt
class VisitView(APIView):

    def post(self, request, format=None):
        try:
            if not request.data.get('visit_reason') or not request.data.get('type'):
                raise ValidationError

            category = Category.objects.get(pk=request.data['type'])
            
                
            serializer = VisitSerializer(data={
                "category": category.id,
                "visit_reason": request.data['visit_reason'],
            })
            
            # TODO: 얼굴인식이 필요할 경우 데이터 형식이 변경되어야 함

            if not serializer.is_valid():
                raise ValidationError

            serializer.save()

            #send_to_firebase_cloud_messaging(
            #   title_msg="방문자 알림",
            #   body_msg=f"{visit_reason}을 위해 누군가가 방문했습니다",
            # )

            return Response(status=status.HTTP_200_OK)
        
        except ValidationError:
            return Response(
                {'detail': 'No required data.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Category.DoesNotExist:
            return Response(
                {'detail': 'Type is not exist'},
                status=status.HTTP_404_NOT_FOUND,
            )


@csrf_exempt
class CategoryListCreateView(APIView):

    def get(self, reqeust, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            if not request.data.get('type'):
                raise ValidationError('No required data.')

            if not isinstance(request.data['type'], str):
                raise ValidationError('Unsupported data type.')

            serializer = CategorySerializer(data=request.data)

            if not serializer.is_valid():
                raise ValidationError

            serializer.save()

            return Response(status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {'detail': e.args[0]},
                status=status.HTTP_400_BAD_REQUEST,
            )


@csrf_exempt
class FCMTokenCreateView(APIView):

    def post(self, request, format=None):
        try:
            if not request.data.get('token'):
                raise ValidationError('No required data.')

            serializer = ClientTokenSerializer(data=request.data)

            if not serializer.is_valid():
                raise ValidationError

            # 테스트 기기는 하나만 사용할 것이기 때문에 혹시 새로운 token을 추가한다면
            # 기존에 있는 토큰은 전부 삭제

            exist_token = ClientToken.objects.all()
            if exist_token.exists():
                exist_token.delete()

            serializer.save()

            return Response(status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {'detail': e.args[0]},
                status=status.HTTP_400_BAD_REQUEST,
            )
