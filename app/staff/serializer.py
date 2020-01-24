from rest_framework import serializers

from core.models import Procedure


class ProcedureSerializer(serializers.ModelSerializer):
    """Serializer for procedure model"""
    image = serializers.ImageField(required=False)

    class Meta:
        model = Procedure
        fields = ('id', 'name', 'speciality', 'image',
                  'days_in_hospital', 'days_in_destination',
                  'duration_minutes', 'overview', 'other_details')
        read_only_fields = ('id', )
