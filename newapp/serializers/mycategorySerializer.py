from newapp.model_s.shopCategoryModel import MyCategory
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class MyCategorySerializer(serializers.ModelSerializer):
    unique_name = serializers.CharField(read_only=True)
    # parent = serializers.PrimaryKeyRelatedField(
    #     queryset=MyCategory.objects.all(), required=False
    # )
    shop = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)

    class Meta:
        model = MyCategory
        fields = "__all__"
        depth = 10

    # def get_children(self, obj):
    #     children = MyCategory.objects.filter(parent=obj)
    #     return NestedMyCategorySerializer(children, many=True).data


class NestedMyCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MyCategory.objects.all(), required=False
    )
    label = serializers.CharField(source="name")
    value = serializers.CharField(read_only=True, source="unique_name")
    shop = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    children = serializers.SerializerMethodField("get_children")

    def get_children(self, obj):
        children = MyCategory.objects.filter(parent=obj)
        return NestedMyCategorySerializer(children, many=True).data
