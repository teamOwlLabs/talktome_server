from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from doorbell.serializers import VisitSerializer, CategorySerializer
from doorbell.models import Category


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
