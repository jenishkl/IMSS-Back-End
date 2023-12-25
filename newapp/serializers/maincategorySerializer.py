from newapp.models import MainCategory
from rest_framework import serializers

class MainCategoryGetSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(), required=False
    )
    unique_name = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(), required=False, write_only=True
    )
    # parent =  serializers.CharField(read_only=True)
