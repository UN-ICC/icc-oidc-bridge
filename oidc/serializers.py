from rest_framework import serializers
from oidc.models import PresentationConfigurations


class PresentationConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationConfigurations

        fields = "__all__"
