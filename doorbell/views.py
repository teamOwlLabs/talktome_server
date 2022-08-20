from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from doorbell.serializers import VisitSerializer
from doorbell.models import Category


@csrf_exempt
class VisitView(APIView):
    def post(self, request, format=None):

        try:
            if not request.data['visit_reason'] or not request.data['type']:
                raise ValidationError

            category = Category.objects.get(type=request.data['type'])
            
                
            serializer = VisitSerializer(data={
                "category": category.id,
                "visit_reason": request.data['visit_reason'],
            })
            
            # TODO: 얼굴인식이 필요할 경우 데이터 형식이 변경되어야 함

            if serializer.is_valid():
                serializer.save()

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
