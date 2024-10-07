from rest_framework import serializers
from .models import Contacts


class ContactstSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'
