from rest_framework import serializers

from doorbell.models import Visit, Category


class VisitSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Visit
    fields = ['id', 'category', 'visit_reason']
    read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):

  class Meta:
    model = Category
    fields = ['id', 'type']
    read_only_fields = ['id']