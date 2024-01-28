from newapp.models import Location
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
dat = True


class LocationSerializer2(serializers.ModelSerializer):
    # id = serializers.PrimaryKeyRelatedField(
    #     queryset=Location.objects.all(), required=False
    # )
    unique_name = serializers.CharField(read_only=True)
    # parent = serializers.PrimaryKeyRelatedField(
    #     queryset=Location.objects.all(), required=False
    # )
    # parent =  serializers.CharField(read_only=True)
    # parent = serializers.SerializerMethodField("get_parent")
    # options = serializers.SerializerMethodField("get_options")

    class Meta:
        model = Location
        fields = "__all__"
        # depth = 2


class LocationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), required=False
    )
    unique_name = serializers.CharField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), required=False, write_only=True
    )
    # parent =  serializers.CharField(read_only=True)
    parent = serializers.SerializerMethodField("get_parent", read_only=True)
    options = serializers.SerializerMethodField("get_options", read_only=True)

    class Meta:
        model = Location
        fields = "__all__"
        depth = 2

    def get_options(self, obj):
        # print(getattr(obj, "parent").id, "ID")
        if getattr(obj, "parent") is not None:
            print(getattr(obj, "parent").id, "Pa2")
        global dat
        if dat:
            if getattr(obj, "parent") is not None:
                parent = Location.objects.filter(parent=getattr(obj, "parent").id)
                print(parent, "options")
                # if  == 0:
                #     return 0
                # dat = False

                return LocationSerializer2(parent, many=True).data
            else:
                # dat = False
                parent = Location.objects.filter(parent=None)
                print(parent, "options2")
                # if  == 0:
                #     return 0
                # dat = False

                return LocationSerializer2(parent, many=True).data

    def get_parent(self, obj):
        # print(getattr(obj, "parent").id, "ID")
        print(obj.parent, "Pa")
        # dat = True
        if obj.parent is not None:
            parent = Location.objects.get(id=getattr(obj, "parent").id)
            print(parent, "Parent")
            # if  == 0:
            #     return 0
            # dat = False

            return LocationSerializer(parent, many=False).data


class NestedLocationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), required=False
    )
    label = serializers.CharField(source="name")
    value = serializers.CharField(read_only=True, source="unique_name")
    children = serializers.SerializerMethodField("get_children")

    def get_children(self, obj):
        children = Location.objects.filter(parent=obj)
        return NestedLocationSerializer(children, many=True).data
