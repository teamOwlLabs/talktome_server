from rest_framework import serializers

from doorbell.models import Visit


class VisitSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Visit
    fields = ['category', 'visit_reason']