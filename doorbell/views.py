import json
import requests

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
from doorbell.models import Category, ClientToken, Visit

def send_to_firebase_cloud_messaging(title_msg, body_msg):
    # Client SDK Token
    registration_token = ClientToken.objects.first().fcm_token

    # TODO: Set Default Message
    message = messaging.Message(

        # 1번 방법
        # notification=messaging.Notification(
        #     title=title_msg,
        #     body=body_msg,
        # ),

        # 2번 방법
        android=messaging.AndroidConfig(
            priority='high',
            notification=messaging.AndroidNotification(
                title=title_msg,
                body=body_msg,
                priority='high',
                visibility='public',
                channel_id='My Channel One1',
            )
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
            try:
                send_to_firebase_cloud_messaging(
              title_msg=category.type,
              body_msg=f"{request.data['visit_reason']}을 위해 누군가가 방문했습니다",)
            except AttributeError: 
                pass

            
            

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
        print(category[0].pictogram)
        serializer = CategorySerializer(category, many=True)

        return Response(serializer.data, 
            status=status.HTTP_200_OK )

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
                raise ValidationError('Post Data Error')

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


@csrf_exempt
class LatestVisitHistoryView(APIView):

    def get(self, request, format=None):
        try:
            unread_visit = Visit.objects.filter(num_of_confirmation=0)

            print(unread_visit)

            # 데이터가 이예 없을 경우 early return
            if not unread_visit.exists():
                return Response(status=status.HTTP_200_OK)

            # 혹시나 그 전에 생성된 방문 기록이지만 안읽고 새로운 방문 기록이 들어온 상황이라면 전에 들어온 것은 같이 읽음 처리
            latest_visit = unread_visit.last()
            category = latest_visit.category

            unread_visit.update(num_of_confirmation=1)

            return Response(
                {
                    'id': latest_visit.id,
                    'category': category.type,
                    'visit_reason': latest_visit.visit_reason,
                    'rgb_color': category.rgb_color,
                    'vibration_pattern': category.vibration_pattern,
                    'pictogram':"/media/"+category.pictogram.name
                },
                status=status.HTTP_200_OK,
            )

        except Exception as _:
            pass


@csrf_exempt
class HostNameView(APIView):

    def get(self, request, format=None):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        result = s.getsockname()[0]
        s.close()

        return Response({'address': result}, status=status.HTTP_200_OK)
